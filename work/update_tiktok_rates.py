from pathlib import Path
p=Path(r'C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site\assets\index-ml-atualizado.js')
js=p.read_text(encoding='utf-8')
old='tiktokshop:{id:"tiktokshop",name:"TikTok Shop",commission:12,fixedFee:2,description:"Taxa TikTok Shop"}'
new='tiktokshop:{id:"tiktokshop",name:"TikTok Shop",commission:6,fixedFee:4,description:"Taxa TikTok Shop"}'
if old not in js:
    raise SystemExit('tiktok config not found')
js=js.replace(old,new,1)
p.write_text(js,encoding='utf-8')
print('updated tiktok shop')
