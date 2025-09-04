import logging
import os
from datetime import datetime

# ==================== 锚定路径 ====================
try:
    fp_root = os.path.join(os.path.dirname(__file__))
    if fp_root.endswith('utils'):
        fp_root = os.path.join(os.path.dirname(fp_root))
    print('fp_root', fp_root)
except NameError:
    fp_root = '.'
def fp_p(*args):
    path = fp_root
    for x in args[:-1]:
        path = os.path.join(path, x)
        if not os.path.exists(path):
            os.mkdir(path)
    return os.path.join(path, args[-1])
# ==================== 配置区 ====================
def dotenv():
    with open(fp_p('.env'), 'r', encoding='utf-8') as env:
        for line in env:
            line = line.strip()
            if line.startswith('//'):
                continue
            tmp = line.split('=', maxsplit=1)
            if len(tmp) <= 1:
                continue
            k, v = tmp[0].strip(), tmp[1].strip()
            if (not k) or (not v):
                continue
            os.environ[k] = v
dotenv()

# 当前日期日志文件
def get_log_file():
    return fp_p('data', 'log', f"{datetime.now().strftime('%Y-%m-%d')}.log")

# ==================== 全局 Logger ====================
logger = logging.getLogger("crypto_monitor")
logger.setLevel(logging.DEBUG)

# 防止重复添加处理器（重要！）
if not logger.handlers:
    # 格式化器：简洁清晰，包含时间、级别、消息
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 文件处理器（自动按天切换，无需轮转库）
    file_handler = logging.FileHandler(get_log_file(), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)