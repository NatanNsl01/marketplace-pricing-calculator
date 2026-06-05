from pathlib import Path
p = Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js = p.read_text(encoding='utf-8')
old = 'k=o==="manual"?parseFloat(i)||0:h.commission,S=o==="manual"?parseFloat(s)||0:h.fixedFee,N=parseFloat(u)||0,O=parseFloat(f)||0,d=cp[g]||0,a=parseFloat(t)||0,m=parseFloat(n)||0,y=parseFloat(r)||0,w=o.startsWith("mercadolivre_")&&parseFloat(mlWeight)>=0?mlFrete(a,parseFloat(mlWeight)):parseFloat(l)||0,C=parseFloat(S)||0'
new = 'k=o==="manual"?parseFloat(i)||0:h.commission,N=parseFloat(u)||0,O=parseFloat(f)||0,d=cp[g]||0,a=parseFloat(t)||0,m=parseFloat(n)||0,y=parseFloat(r)||0,S=o.startsWith("mercadolivre_")&&parseFloat(mlWeight)>=0?mlFrete(a,parseFloat(mlWeight)):o==="manual"?parseFloat(s)||0:h.fixedFee,w=parseFloat(l)||0,C=parseFloat(S)||0'
if old not in js:
    raise SystemExit('target calculation block not found')
js = js.replace(old, new, 1)
js = js.replace('placeholder:a.marketplace&&a.marketplace.startsWith("mercadolivre_")?"automático":"10.00"', 'placeholder:"10.00"', 1)
p.write_text(js, encoding='utf-8')
print('updated')
