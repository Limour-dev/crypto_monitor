import sys, os, time, random
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from exchange.hyperliquid.order import sell_min, buy_min, schedule_cancel
from exchange.hyperliquid.info import l2Book
all = 0
while True:
    ask, bid = l2Book('ETH')
    if bid[0][0] < 4350:
        print('skip', bid[0][0])
        time.sleep(random.randint(20, 30))
        continue
    res = sell_min('ETH', max(bid, key=lambda x:x[1])[0])
    all += 1
    print(all, res)
    res = schedule_cancel(30 * 1000)
    print(res)
    if all > 30:
        break
    time.sleep(random.randint(30, 60))

if False:
    from exchange.hyperliquid.order import account, address
    from hyperliquid.exchange import Exchange
    from hyperliquid.info import Info
    from hyperliquid.utils import constants
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    print(info.name_to_asset('BTC'))  # 0
    print(info.name_to_asset('ETH'))  # 1
    ex = Exchange(account, constants.MAINNET_API_URL, account_address=address)
    res = ex.order(
        'ETH',
        False,
        0.01,
        4800,
        ORDER_ALO
    )