from pathlib import Path
p=Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js=p.read_text(encoding='utf-8')
old='c.jsx(Kt,{icon:lu,label:"Total de Taxas",value:Ee(w.totalFees),color:"orange"})'
new='c.jsx(TaxasCard,{icon:lu,result:w,product:a})'
if old not in js:
    raise SystemExit('taxes card call not found')
js=js.replace(old,new,1)
marker='function Kt({icon:e,label:t,value:n,color:r}){'
component='function TaxasCard({icon:e,result:t,product:n}){const r={orange:"bg-orange-500/10 text-orange-400 border-orange-500/30"},l=Number(n.sellingPrice)||0,o=Number(n.customTax)||0,i=Number(n.customDiscount)||0,s=l*(t.commission/100),u=l*(o/100),f=l*(i/100);return c.jsxs("div",{className:`bg-slate-800/50 backdrop-blur rounded-xl border p-4 ${r.orange}`,children:[c.jsxs("div",{className:"flex items-center gap-2 mb-2",children:[c.jsx(e,{className:"w-4 h-4"}),c.jsx("span",{className:"text-sm font-medium opacity-80",children:"Total de Taxas"})]}),c.jsxs("div",{className:"space-y-1 mb-2 text-xs opacity-80",children:[c.jsxs("div",{className:"flex justify-between gap-2",children:[c.jsx("span",{children:`Comissão (${t.commission}%)`}),c.jsx("span",{children:Ee(s)})]}),c.jsxs("div",{className:"flex justify-between gap-2",children:[c.jsx("span",{children:"Taxa fixa"}),c.jsx("span",{children:Ee(t.fixedFee)})]}),o>0&&c.jsxs("div",{className:"flex justify-between gap-2",children:[c.jsx("span",{children:`Imposto (${o}%)`}),c.jsx("span",{children:Ee(u)})]}),i>0&&c.jsxs("div",{className:"flex justify-between gap-2",children:[c.jsx("span",{children:`Desconto (${i}%)`}),c.jsx("span",{children:Ee(f)})]})]}),c.jsx("p",{className:"text-xl font-bold",children:Ee(t.totalFees)})]})}'
if marker not in js:
    raise SystemExit('Kt marker not found')
js=js.replace(marker,component+marker,1)
p.write_text(js,encoding='utf-8')
print('updated fees composition')
