Write-Host "==================================="
Write-Host "LongPort 量化交易系统"
Write-Host "==================================="

$pythonCandidates = @("python", "python3", "py")
$pythonCommand = $null
foreach ($candidate in $pythonCandidates) {
    try {
        $command = Get-Command $candidate -ErrorAction Stop
        $pythonCommand = $command.Path
        break
    } catch {
        continue
    }
}

if (-not $pythonCommand) {
    Write-Error "未找到可用的 Python 解释器。请先安装 Python 并确保其已加入 PATH。"
    exit 1
}

if (-not (Test-Path -Path ".env")) {
    Write-Error "未找到 .env 配置文件，请在项目根目录创建后再运行。"
    exit 1
}

Write-Host "初始化数据库..."
& $pythonCommand "backend/init_db.py"
if ($LASTEXITCODE -ne 0) {
    Write-Error "数据库初始化失败。您可以单独运行 '$pythonCommand backend/init_db.py' 进行调试。"
    exit $LASTEXITCODE
}

Write-Host "==================================="
Write-Host "启动 FastAPI 服务器..."
& $pythonCommand "backend/server.py"
