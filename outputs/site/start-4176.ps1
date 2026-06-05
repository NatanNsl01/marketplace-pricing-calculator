$ErrorActionPreference = "Stop"
$env:PORT = "4176"
Set-Location -LiteralPath "C:\Users\natan\Documents\Codex\2026-06-05\https-pricing-calculator2-beta-vercel-app\outputs\site"
& "C:\Users\natan\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" "server.cjs"
