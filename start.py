"""Cross-platform launcher for the PawQuant Trade backend."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / "backend"
INIT_SCRIPT = BACKEND_DIR / "init_db.py"
SERVER_SCRIPT = BACKEND_DIR / "server.py"


def ensure_env_file() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        raise FileNotFoundError(
            "未找到 .env 配置文件，请先在项目根目录创建并填写 API 与数据库配置。"
        )


def run_subprocess(script: Path) -> int:
    command = [sys.executable, str(script)]
    process = subprocess.run(command, check=False)
    return process.returncode


def main() -> int:
    print("===================================")
    print("LongPort 量化交易系统")
    print("===================================")

    try:
        ensure_env_file()
    except FileNotFoundError as exc:
        print(exc)
        return 1

    print("初始化数据库...")
    init_code = run_subprocess(INIT_SCRIPT)
    if init_code != 0:
        print("数据库初始化失败，请检查配置或单独运行下面的命令排查:")
        print(f"  {sys.executable} {INIT_SCRIPT}")
        return init_code

    print("===================================")
    print("启动 FastAPI 服务器...")

    try:
        return run_subprocess(SERVER_SCRIPT)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
