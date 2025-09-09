from logging.handlers import RotatingFileHandler
import logging
import os
from colorama import Fore, Back, Style, init

#####
#🔥📌✅📂📄🔹🎨😃🚀❌🔧⚠📁🗑️🔇🛑🎙️🎤

C = {
    "red": "\033[91m", "green": "\033[92m", "blue": "\033[94m",
    "yellow": "\033[93m", "cyan": "\033[96m", "magenta": "\033[95m",
    "black": "\033[30m", "white": "\033[97m", "gray": "\033[37m",
    "orange": "\033[33m", "purple": "\033[35m", "pink": "\033[95m",

    # 背景色
    "bg_red": "\033[41m", "bg_green": "\033[42m", "bg_blue": "\033[44m",
    "bg_yellow": "\033[43m", "bg_cyan": "\033[46m", "bg_magenta": "\033[45m",
    "bg_black": "\033[40m", "bg_white": "\033[47m",

    "r": "\033[0m"
}


# 初始化 colorama（Windows 也能支援 ANSI 色碼）
init(autoreset=True)

# 不同 log level 的顏色對應
_LEVEL_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    # CRITICAL 只在以下 formatter 中特別處理
}

# 預設的格式字串
_DEFAULT_FMT = "[{asctime}] [{name}] {level_color}{levelname}{reset} | {message}"
_DATE_FMT = "%m/%d %H:%M"

class LevelFormatter(logging.Formatter):
    """依 record.levelno 動態套用顏色與格式，對 CRITICAL 進行全行背景紅色且訊息包 ❌"""

    def __init__(self, fmt=_DEFAULT_FMT, datefmt=_DATE_FMT):
        super().__init__(fmt=fmt, datefmt=datefmt, style='{')

    def format(self, record):
        # 先讓 base class 填好 asctime, name, levelname, message
        if record.levelno == logging.CRITICAL:
            # 包裝訊息
            message = f"❌{record.getMessage()}❌"

            # 手動組好時間
            asctime = self.formatTime(record, self.datefmt)
            # 組出未上色的字串
            text = f"[{asctime}] [{record.name}] {record.levelname} | {message}"
            # 全行背景紅、前景白，最後 reset
            return f"{Back.RED}{Fore.WHITE}{text}{Style.RESET_ALL}"
        else:
            # 非 CRITICAL 使用既有顏色對應
            level_color = _LEVEL_COLORS.get(record.levelno, "")
            reset = Style.RESET_ALL
            record.level_color = level_color
            record.reset = reset
            # message 屬性預設就是 record.getMessage()
            record.message = record.getMessage()
            return super().format(record)

def get_logger(
    name: str = "main",
    level: int = logging.DEBUG,
    log_dir: str | None = None,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 3,
    format: str = None
) -> logging.Logger:
    """
    建立並回傳一個 logger：
    
    - name: logger 名稱
    - level: logging level
    - log_dir: 若提供，會在此資料夾內建立 rotating file logs
    - max_bytes、backup_count: 用於 RotatingFileHandler
    """

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # 已初始化過，就直接回傳

    logger.setLevel(level)
    formatter = LevelFormatter()

    # 1) Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 2) File handler (若 log_dir 給定)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        file_path = os.path.join(log_dir, f"{name}.log")
        fh = RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


# 範例測試
if __name__ == "__main__":
    log = get_logger()
    log.debug("這是 debug 訊息")
    log.info("這是 info 訊息")
    log.warning("這是 warning 訊息")
    log.error("這是 error 訊息")
    log.critical("這是 critical 訊息")