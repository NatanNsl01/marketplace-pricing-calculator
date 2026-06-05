from pathlib import Path
p = Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js = p.read_text(encoding='utf-8')
if 'const shopeeTaxas=' not in js:
    old = '];const mlPeso='
    new = '];const shopeeTaxas=[[0,7.99,0,3.995],[8,79.99,20,4],[80,99.99,14,16],[100,199.99,14,20],[200,499.99,14,26],[500,9999999,14,26]];function shopeeTaxa(e){if(!(e>0))return{commission:0,fixedFee:0};const t=shopeeTaxas.find(n=>e>=n[0]&&e<=n[1])||shopeeTaxas[shopeeTaxas.length-1];return{commission:t[2],fixedFee:t[3]}}const mlPeso='
    if old not in js:
        raise SystemExit('insert marker not found')
    js = js.replace(old, new, 1)
old_calc = 'k=o==="manual"?parseFloat(i)||0:h.commission,N=parseFloat(u)||0,O=parseFloat(f)||0,d=cp[g]||0,a=parseFloat(t)||0,m=parseFloat(n)||0,y=parseFloat(r)||0,S=o.startsWith("mercadolivre_")&&parseFloat(mlWeight)>=0?mlFrete(a,parseFloat(mlWeight)):o==="manual"?parseFloat(s)||0:h.fixedFee,w=parseFloat(l)||0,C=parseFloat(S)||0'
new_calc = 'N=parseFloat(u)||0,O=parseFloat(f)||0,d=cp[g]||0,a=parseFloat(t)||0,m=parseFloat(n)||0,y=parseFloat(r)||0,sh=o==="shopee"?shopeeTaxa(a):null,k=sh?sh.commission:o==="manual"?parseFloat(i)||0:h.commission,S=sh?sh.fixedFee:o.startsWith("mercadolivre_")&&parseFloat(mlWeight)>=0?mlFrete(a,parseFloat(mlWeight)):o==="manual"?parseFloat(s)||0:h.fixedFee,w=parseFloat(l)||0,C=parseFloat(S)||0'
if old_calc in js:
    js = js.replace(old_calc, new_calc, 1)
elif new_calc not in js:
    raise SystemExit('calculation block not found')
p.write_text(js, encoding='utf-8')
print('updated shopee')
