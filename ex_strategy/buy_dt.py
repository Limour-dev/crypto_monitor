import sys, os, time, random, traceback
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from exchange.hyperliquid.order import sell_min, buy_min, schedule_cancel, address
from exchange.hyperliquid.info import l2Book, clearinghouseState

while True:
    try:
        st = clearinghouseState(address)
        aP = st['assetPositions']
        for aPo in aP:
            position = aPo['position']
            coin = position['coin']
            entryPx = float(position['entryPx'])
            positionValue = float(position['positionValue'])
            ask, bid = l2Book(coin)
            gpx = max(bid, key=lambda x: x[1])[0] * 1.0005
            if bid[0][0] < entryPx or positionValue < 500:
                print('skip', bid[0][0], positionValue, gpx)
                time.sleep(random.randint(20, 30))
                continue
            res = sell_min(coin, gpx)
        time.sleep(random.randint(30, 60))
    except:
        traceback.print_last()