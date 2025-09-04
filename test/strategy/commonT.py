import sys, os
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from utils.logger import fp_p
from utils.ohlcvDB import KLineDB, ft2ts
kdb = KLineDB(fp_p('data', 'ETHUSDT', 'P.db'))

src = kdb.latest_1h(150)
src = [k.c for k in src[::-1]]

from strategy.common import f_log_regression, ta_stdev
middle = f_log_regression(src)[1]
st_dev = ta_stdev(src)
upper = middle + 1.5 * st_dev
lower = middle - 1.5 * st_dev