import sys, os
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from utils.logger import fp_p
from utils.ohlcvDB import KLineDB, ft2ts
kdb = KLineDB(fp_p('data', 'ETHUSDT', 'P.db'))
print(kdb.earliest())
print(kdb.latest_1h())