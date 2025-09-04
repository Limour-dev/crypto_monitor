import sys, os
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from utils.http_client import http_client

resp = http_client.get('https://fapi.binance.com/fapi/v1/time')