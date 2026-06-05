from pathlib import Path
p=Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js=p.read_text(encoding='utf-8')
js=js.replace('Object.values(Je).map(p=>c.jsx("option",{value:p.id,children:p.name},p.id))','Object.values(Je).filter(p=>!["amazon","shein"].includes(p.id)).map(p=>c.jsx("option",{value:p.id,children:p.name},p.id))')
js=js.replace('Suporta: Shopee, Mercado Livre, Amazon, TikTok Shop, Shein','Suporta: Shopee, Mercado Livre, TikTok Shop')
p.write_text(js,encoding='utf-8')
print('removed amazon shein from visible marketplace options')
