from exchange.binance.api import Future
from utils.http_client import http_client

from typing import Union, List, Any

def get_klines(pair: str,  interval: str = '1m', limit: int = 500,
                          start_time: int = None, end_time: int = None) -> Union[List[Any], None]:
    """获取连续合约K线数据"""
    params = {"pair": pair, "contractType": "PERPETUAL", "interval": interval, "limit": limit}
    if start_time:
        params["startTime"] = start_time
    if end_time:
        params["endTime"] = end_time
    return http_client.get(Future.CONTINUOUS_KLINE, params=params)

def get_time():
    return http_client.get('https://fapi.binance.com/fapi/v1/time')['serverTime']