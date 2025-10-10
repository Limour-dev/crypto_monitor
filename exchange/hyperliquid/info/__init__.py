from utils.http_client import http_client
url = r'https://api.hyperliquid.xyz/info'

def meta():
    res = http_client.post(url, data={
        'type': 'meta'
    })
    return res

def perpDexs():
    res = http_client.post(url, data={
        'type': 'perpDexs'
    })
    return res

def clearinghouseState(user):
    res = http_client.post(url, data={
        'type': 'clearinghouseState',
        'user': user
    })
    return res

def l2Book(coin):
    res = http_client.post(url, data={
        'type': 'l2Book',
        'coin': coin
    })
    levels = res.get('levels', [[], []])
    bid = [(float(x['px']), float(x['sz'])) for x in levels[1]]
    ask = [(float(x['px']), float(x['sz'])) for x in levels[0]]
    bid.sort(key=lambda x:x[0])
    ask.sort(key=lambda x:x[0], reverse=True)
    return ask, bid