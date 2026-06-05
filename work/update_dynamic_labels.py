from pathlib import Path
p = Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js = p.read_text(encoding='utf-8')
js = js.replace('a.marketplace!=="manual"&&`(${(E=Je[a.marketplace])==null?void 0:E.commission}%)`', 'a.marketplace!=="manual"&&`(${w.commission}%)`', 1)
js = js.replace('a.marketplace!=="manual"&&`(${(z=Je[a.marketplace])==null?void 0:z.fixedFee})`', 'a.marketplace!=="manual"&&`(${w.fixedFee})`', 1)
p.write_text(js, encoding='utf-8')
print('labels updated')
