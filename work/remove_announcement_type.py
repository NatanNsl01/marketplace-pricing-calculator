from pathlib import Path
p = Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js = p.read_text(encoding='utf-8')
start_marker = 'c.jsxs("div",{className:"grid grid-cols-2 gap-4",children:[c.jsxs("div",{children:[c.jsx("label",{className:"block text-sm font-medium text-slate-300 mb-1",children:"Marketplace"})'
tipo_marker = '),c.jsxs("div",{children:[c.jsx("label",{className:"block text-sm font-medium text-slate-300 mb-1",children:"Tipo de Anúncio"})'
cat_marker = '),c.jsxs("div",{children:[c.jsx("label",{className:"block text-sm font-medium text-slate-300 mb-1",children:"Categoria"})'
start = js.index(start_marker)
tipo = js.index(tipo_marker, start)
end = js.index(cat_marker, tipo)
marketplace_child = js[start + len('c.jsxs("div",{className:"grid grid-cols-2 gap-4",children:['):tipo]
replacement = marketplace_child
js = js[:start] + replacement + js[end:]
p.write_text(js, encoding='utf-8')
print('removed announcement type field')
