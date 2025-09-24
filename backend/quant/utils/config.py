import os
from pathlib import Path

from dotenv import load_dotenv
from longport.openapi import Config

# 加载环境变量
load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[3]
DEFAULT_LOG_DIR = BASE_DIR / "logs"
DEFAULT_TASK_LOG_DIR = DEFAULT_LOG_DIR / "tasks"
DEFAULT_SERVER_LOG_FILE = DEFAULT_LOG_DIR / "server.log"


class ServerConfig:
    def __init__(self):
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", 8000))

        task_log_dir_env = os.getenv("TASK_LOG_DIR")
        task_log_dir = (
            Path(task_log_dir_env).expanduser()
            if task_log_dir_env
            else DEFAULT_TASK_LOG_DIR
        )
        task_log_dir.mkdir(parents=True, exist_ok=True)
        self.task_log_dir = str(task_log_dir)

        server_log_file_env = os.getenv("SERVER_LOG_FILE")
        server_log_file = (
            Path(server_log_file_env).expanduser()
            if server_log_file_env
            else DEFAULT_SERVER_LOG_FILE
        )
        server_log_file.parent.mkdir(parents=True, exist_ok=True)
        self.server_log_file = str(server_log_file)

        self.server_log_level = os.getenv("SERVER_LOG_LEVEL", "INFO")


class LongPortConfig:
    def __init__(self):
        self.quote_ws_url = os.getenv("LONGPORT_QUOTE_URL")
        self.trade_ws_url = os.getenv("LONGPORT_TRADE_URL")
        self.http_url = os.getenv("LONGPORT_HTTP_URL")

        # 实盘配置
        self.live_app_key = os.getenv("LONGPORT_LIVE_APP_KEY")
        self.live_app_secret = os.getenv("LONGPORT_LIVE_APP_SECRET")
        self.live_access_token = os.getenv("LONGPORT_LIVE_ACCESS_TOKEN")

        # 模拟盘配置
        self.paper_app_key = os.getenv("LONGPORT_PAPER_APP_KEY")
        self.paper_app_secret = os.getenv("LONGPORT_PAPER_APP_SECRET")
        self.paper_access_token = os.getenv("LONGPORT_PAPER_ACCESS_TOKEN")

    def get_config(self, is_paper=False):
        """获取长桥配置对象"""
        if is_paper:
            return Config(
                app_key=self.paper_app_key,
                app_secret=self.paper_app_secret,
                access_token=self.paper_access_token,
                http_url=self.http_url,
                quote_ws_url=self.quote_ws_url,
                trade_ws_url=self.trade_ws_url,
            )
        else:
            return Config(
                app_key=self.live_app_key,
                app_secret=self.live_app_secret,
                access_token=self.live_access_token,
                http_url=self.http_url,
                quote_ws_url=self.quote_ws_url,
                trade_ws_url=self.trade_ws_url,
            )


class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", 3306))
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE", "Stock")

    def get_connection_url(self):
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# 全局配置实例
server_config = ServerConfig()
db_config = DatabaseConfig()


_longport_config = LongPortConfig()
paper_longport_config = _longport_config.get_config(is_paper=True)
live_longport_config = _longport_config.get_config(is_paper=False)
