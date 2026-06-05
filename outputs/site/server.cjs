const http = require("http");
const fs = require("fs");
const path = require("path");

const root = __dirname;
const port = Number(process.env.PORT || 4173);

const types = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

function send(res, status, body, headers = {}) {
  res.writeHead(status, {
    "Access-Control-Allow-Origin": "*",
    ...headers,
  });
  res.end(body);
}

function serveFile(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const requested = decodeURIComponent(url.pathname === "/" ? "/index.html" : url.pathname);
  const filePath = path.resolve(root, `.${requested}`);

  if (!filePath.startsWith(root)) {
    send(res, 403, "Forbidden");
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      send(res, 404, "Not found");
      return;
    }

    const contentType = types[path.extname(filePath).toLowerCase()] || "application/octet-stream";
    send(res, 200, data, { "Content-Type": contentType });
  });
}

async function proxyMercadoLivre(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const target = url.searchParams.get("url");

  if (!target || !/^https:\/\/api\.mercadolibre\.com\//.test(target)) {
    send(res, 400, JSON.stringify({ error: "URL inválida" }), {
      "Content-Type": "application/json; charset=utf-8",
    });
    return;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12000);

  try {
    const response = await fetch(target, {
      signal: controller.signal,
      headers: {
        Accept: "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        Origin: "https://www.mercadolivre.com.br",
        Referer: "https://www.mercadolivre.com.br/",
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
      },
    });

    const body = await response.text();
    send(res, response.status, body, {
      "Content-Type": response.headers.get("content-type") || "application/json; charset=utf-8",
    });
  } catch (error) {
    send(res, 502, JSON.stringify({ error: error.message || "Falha no proxy" }), {
      "Content-Type": "application/json; charset=utf-8",
    });
  } finally {
    clearTimeout(timeout);
  }
}

function pickJsonLd(html) {
  const scripts = html.match(
    /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi
  );

  if (!scripts) return null;

  for (const script of scripts) {
    const raw = script
      .replace(/^[\s\S]*?>/, "")
      .replace(/<\/script>[\s\S]*$/i, "")
      .trim();

    try {
      const data = JSON.parse(raw);
      const items = Array.isArray(data) ? data : [data];
      const product = items.find((item) => item && item["@type"] === "Product");
      if (product) return product;
    } catch {
      // Some pages include non-product JSON-LD; skip invalid blocks.
    }
  }

  return null;
}

function metaContent(html, property) {
  const direct = new RegExp(
    `<meta[^>]+(?:property|name)=["']${property}["'][^>]+content=["']([^"']+)["'][^>]*>`,
    "i"
  );
  const reverse = new RegExp(
    `<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["']${property}["'][^>]*>`,
    "i"
  );
  const match = html.match(direct) || html.match(reverse);
  return match ? decodeHtml(match[1]) : "";
}

function decodeHtml(value) {
  return String(value || "")
    .replace(/&quot;/g, '"')
    .replace(/&#34;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}

function regexValue(html, patterns) {
  for (const pattern of patterns) {
    const match = html.match(pattern);
    if (match && match[1]) return decodeHtml(match[1]);
  }
  return "";
}

function normalizeWhitespace(value) {
  return decodeHtml(value).replace(/\s+/g, " ").trim();
}

async function scrapeMercadoLivrePage(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const target = url.searchParams.get("url");

  if (!target || !/^https:\/\/([^/]+\.)?mercadolivre\.com(\.br)?\//.test(target)) {
    send(res, 400, JSON.stringify({ error: "URL inválida", target }), {
      "Content-Type": "application/json; charset=utf-8",
    });
    return;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12000);

  try {
    const response = await fetch(target, {
      signal: controller.signal,
      headers: {
        Accept: "text/html,application/xhtml+xml",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
      },
    });

    const html = await response.text();
    const product = pickJsonLd(html) || {};
    const offers = Array.isArray(product.offers) ? product.offers[0] : product.offers || {};
    const title =
      product.name ||
      metaContent(html, "og:title") ||
      regexValue(html, [
        /"title"\s*:\s*"([^"]+)"/i,
        /<h1[^>]*>([^<]+)<\/h1>/i,
        /<title[^>]*>([^<]+)<\/title>/i,
      ]);
    const price =
      offers.price ||
      metaContent(html, "product:price:amount") ||
      regexValue(html, [
        /"price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?/i,
        /"amount"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?/i,
      ]);
    const permalink = product.url || metaContent(html, "og:url") || target;
    const categoryId = regexValue(html, [
      /"category_id"\s*:\s*"([^"]+)"/i,
      /"categoryId"\s*:\s*"([^"]+)"/i,
    ]);
    const categoryName = normalizeWhitespace(
      product.category ||
        metaContent(html, "product:category") ||
        regexValue(html, [
          /"category_name"\s*:\s*"([^"]+)"/i,
          /"categoryName"\s*:\s*"([^"]+)"/i,
          /"category"\s*:\s*\{\s*"name"\s*:\s*"([^"]+)"/i,
          /<a[^>]+class=["'][^"']*(?:breadcrumb|andes-breadcrumb)[^"']*["'][^>]*>([^<]+)<\/a>/i,
        ])
    );

    if ((!title && !price) || (title === "Mercado Libre" && !price)) {
      send(res, 404, JSON.stringify({ error: "Dados não encontrados", status: response.status }), {
        "Content-Type": "application/json; charset=utf-8",
      });
      return;
    }

    send(
      res,
      200,
      JSON.stringify({
        title,
        name: title,
        price,
        category_id: categoryId,
        category_name: categoryName,
        category: categoryName,
        permalink,
      }),
      { "Content-Type": "application/json; charset=utf-8" }
    );
  } catch (error) {
    send(res, 502, JSON.stringify({ error: error.message || "Falha ao ler anúncio" }), {
      "Content-Type": "application/json; charset=utf-8",
    });
  } finally {
    clearTimeout(timeout);
  }
}

http
  .createServer((req, res) => {
    if (req.url.startsWith("/api/ml-page")) {
      scrapeMercadoLivrePage(req, res);
      return;
    }

    if (req.url.startsWith("/api/ml")) {
      proxyMercadoLivre(req, res);
      return;
    }

    serveFile(req, res);
  })
  .listen(port, () => {
    console.log(`Calculadora disponível em http://localhost:${port}`);
  });
