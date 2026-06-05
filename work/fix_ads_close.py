from pathlib import Path
p=Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js=p.read_text(encoding='utf-8')
js=js.replace('placeholder:"0"})]}]}),c.jsxs("div",{className:"mt-6 flex gap-3"', 'placeholder:"0"})]})] }),c.jsxs("div",{className:"mt-6 flex gap-3"'.replace('] })', ']})'), 1)
p.write_text(js, encoding='utf-8')
print('fixed close')
