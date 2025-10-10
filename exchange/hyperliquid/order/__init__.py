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
    if px > 100000:
        px = int(px)
    return order(
        name = name,
        is_buy = True,
        sz = math.ceil(min_val / px * 100000) / 100000,
        limit_px = px,
        order_type = ORDER_ALO
    )

def sell_min(name: str, px: float):
    if px > 100000:
        px = int(px)
    return order(
        name = name,
        is_buy = False,
        sz = math.ceil(min_val / px * 100000) / 100000,
        limit_px = px,
        order_type = ORDER_ALO
    )


def schedule_cancel(delta_time: int) -> Any:
    """Schedules a time (in UTC millis) to cancel all open orders. The time must be at least 5 seconds after the current time.
    Once the time comes, all open orders will be canceled and a trigger count will be incremented. The max number of triggers
    per day is 10. This trigger count is reset at 00:00 UTC.

    Args:
        time (int): if time is not None, then set the cancel time in the future. If None, then unsets any cancel time in the future.
    """
    timestamp = get_timestamp_ms()
    schedule_cancel_action = {
        "type": "scheduleCancel",
        "time": timestamp + delta_time
    }

    signature = sign_l1_action(
        account,
        schedule_cancel_action,
        None,
        timestamp,
        None,
        True
    )

    data =  {
        'action': schedule_cancel_action,
        'nonce': timestamp,
        'signature': signature
    }

    res = http_client.post(url, data=data)

    return res