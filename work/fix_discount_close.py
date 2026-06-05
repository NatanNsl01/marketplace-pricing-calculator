from pathlib import Path
p=Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js=p.read_text(encoding='utf-8')
old='placeholder:"0"})]}])}),c.jsxs("div",{className:"mt-6 flex gap-3"'
new='placeholder:"0"})]})]}),c.jsxs("div",{className:"mt-6 flex gap-3"'
if old not in js:
    raise SystemExit('pattern not found')
js=js.replace(old,new,1)
p.write_text(js,encoding='utf-8')
print('fixed pattern')
