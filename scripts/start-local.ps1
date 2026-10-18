$siteRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $siteRoot
$devReady = $false
try { $devReady = (Invoke-WebRequest 'http://127.0.0.1:4321/' -UseBasicParsing -TimeoutSec 2).StatusCode -eq 200 } catch {}
if (-not $devReady) { & npm.cmd run dev }
$cmsReady = $false
try { $cmsReady = (Invoke-WebRequest 'http://127.0.0.1:8081/api/v1' -Method Post -ContentType 'application/json' -Body '{"action":"info"}' -UseBasicParsing -TimeoutSec 2).StatusCode -eq 200 } catch {}
if (-not $cmsReady) { Start-Process -FilePath (Get-Command node.exe).Source -ArgumentList 'scripts/start-cms.mjs' -WorkingDirectory $siteRoot -WindowStyle Hidden }
Write-Output 'Website: http://127.0.0.1:4321/'
Write-Output 'CMS: http://127.0.0.1:4321/admin/'
