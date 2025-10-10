import os

from utils.http_client import http_client
import eth_account
from hyperliquid.utils.types import *
from hyperliquid.utils.signing import *
import math

account = eth_account.Account.from_key(os.environ.get('HYPE_KEY'))
address = os.environ.get('HYPE_USR')
if address == "":
    address = account.address
print("HYPE running with account address:", address)

ORDER_ALO = {'limit': {'tif': 'Alo'}}
name2asset = {
    'BTC': 0,
    'ETH': 1
}
url = r'https://api.hyperliquid.xyz/exchange'

def order(
        name: str,
        is_buy: bool,
        sz: float,
        limit_px: float,
        order_type: OrderType,
        reduce_only: bool = False,
) -> Any:

    porder = {
        'a': name2asset.get(name),
        'b': is_buy,
        'p': str(limit_px),
        's': str(sz),
        'r': reduce_only,
        't': order_type
    }

    order_action = {
        'type': 'order',
        'orders': [porder],
        'grouping': 'na'
    }

    timestamp = get_timestamp_ms()

    signature = sign_l1_action(
        account,
        order_action,
        None,
        timestamp,
        None,
        True
    )

    data = {
        'action': order_action,
        'nonce': timestamp,
        'signature': signature
    }

    res = http_client.post(url, data=data)

    return res

min_val = 15

def buy_min(name: str, px: float):
    return order(
        name = name,
        is_buy = True,
        sz = math.ceil(min_val / px * 10000) / 10000,
        limit_px = px,
        order_type = ORDER_ALO
    )

def sell_min(name: str, px: float):
    return order(
        name = name,
        is_buy = False,
        sz = math.ceil(min_val / px * 10000) / 10000,
        limit_px = px,
        order_type = ORDER_ALO
    )