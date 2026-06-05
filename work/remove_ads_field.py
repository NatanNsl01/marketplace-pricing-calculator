from pathlib import Path
p = Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js = p.read_text(encoding='utf-8')
# Neutralize ad percentage calculation regardless of stored state.
js = js.replace('O=parseFloat(f)||0,d=cp[g]||0,a=parseFloat(t)||0', 'O=parseFloat(f)||0,d=0,a=parseFloat(t)||0', 1)
# Remove the visual Anúncios (%) select, leaving Imposto and Desconto in a 2-column row.
start_marker = 'c.jsxs("div",{className:"grid grid-cols-3 gap-4",children:[c.jsxs("div",{children:[c.jsx("label",{className:"block text-sm font-medium text-slate-300 mb-1",children:"Imposto (%)"})'
ad_marker = '),c.jsxs("div",{children:[c.jsx("label",{className:"block text-sm font-medium text-slate-300 mb-1",children:"Anúncios (%)"})'
end_marker = ']}),c.jsxs("div",{className:"mt-6 flex gap-3"'
start = js.index(start_marker)
ad = js.index(ad_marker, start)
end = js.index(end_marker, ad)
first_two = js[start:ad]
first_two = first_two.replace('className:"grid grid-cols-3 gap-4"', 'className:"grid grid-cols-2 gap-4"', 1)
replacement = first_two + end_marker
js = js[:start] + replacement + js[end+len(end_marker):]
p.write_text(js, encoding='utf-8')
print('removed ads field')
