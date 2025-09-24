import logging
from pathlib import Path

from .config import server_config


SUCCESS = 25


class LevelSignFormatter(logging.Formatter):
    """自定义日志格式化器，添加不同级别的标志"""

    LEVEL_SIGNS = {
        logging.DEBUG: "🐞",
        logging.INFO: "ℹ️",
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🔥",
        SUCCESS: "✅",
    }

    def format(self, record):
        record.levelsign = self.LEVEL_SIGNS.get(record.levelno, "")
        return super().format(record)


base_logger = logging.getLogger()
base_logger.setLevel(server_config.server_log_level)
console_handler = logging.StreamHandler()
console_handler.setLevel(server_config.server_log_level)
formatter = LevelSignFormatter("[%(asctime)s] %(levelsign)s [%(name)s] %(message)s")
console_handler.setFormatter(formatter)
base_logger.addHandler(console_handler)

server_log_file = Path(server_config.server_log_file)
try:
    server_log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(server_log_file)
    file_handler.setLevel(server_config.server_log_level)
    file_handler.setFormatter(formatter)
    base_logger.addHandler(file_handler)
except (OSError, ValueError) as error:
    base_logger.warning(
        "日志文件创建失败，继续使用控制台输出: %s", error
    )
