import sys, os, time
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)
from exchange.binance.market.future.kline import get_klines, get_time

from utils.logger import fp_p
from utils.ohlcvDB import KLineDB, ft2ts, binance_p

def main(symbol):
    kdb = KLineDB(fp_p('data', symbol, 'P.db'))
    now = get_time()
    tmp = get_klines(symbol, end_time=kdb.earliest()[0].ts)
    for bar in tmp[::-1]:
        if bar[6] - now > 0: # 不完整的k线
            continue
        k = binance_p(bar)
        kdb.insert(k, False)
    kdb.commit()
    print(kdb.earliest())
for i in range(240):
    main('ETHUSDT')
    time.sleep(3)
