import sys, os, time, random, traceback
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from exchange.hyperliquid.order import sell_min, buy_min, schedule_cancel
from exchange.hyperliquid.info import l2Book

all = 0
while True:
    try:
        ask, bid = l2Book('BTC')
        if ask[0][0] > 117600:
            print('skip', ask[0][0])
            time.sleep(random.randint(20, 30))
            continue
        res = buy_min('BTC', max(ask, key=lambda x:x[1])[0])
        all += 1
        print(all, res)
        res = schedule_cancel(30 * 1000)
        print(res)
        if all > 30:
            break
        time.sleep(random.randint(30, 60))
    except:
        traceback.print_last()