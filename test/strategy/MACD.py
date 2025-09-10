# ====== 环境配置 ======
import sys, os
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from utils.logger import fp_p
from utils.ohlcvDB import KLineDB
kdb = KLineDB(fp_p('data', 'BTCUSDT', 'P.db'))
from strategy.common import macd, ta_stdev
# ====== 计算 ======
# 需要先执行 test/getMoreData.py 获取足够的数据
bars = kdb.latest_1h(200 + 200)
src = [bar.c for bar in bars]
macd_line = macd(src)[-200:]
middle = sum(macd_line) / 200
stdev = ta_stdev(macd_line)
