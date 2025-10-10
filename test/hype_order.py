import sys, os, time
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from exchange.hyperliquid.order import sell_min, buy_min
from exchange.hyperliquid.info import l2Book
for i in range(10):
    ask, bid = l2Book('ETH')
    res = sell_min('ETH', bid[-1][0] + 100)
    time.sleep(60)

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