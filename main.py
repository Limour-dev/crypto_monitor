from utils.logger import fp_p, logger
from notify.wechat_bot import wechat_push
from exchange.binance.market.future.kline import get_klines, get_time
from utils.ohlcvDB import KLineDB, ft2ts, binance_p

symbols = {
    'ETHUSDT': KLineDB(fp_p('data', 'ETHUSDT', 'P.db')),
    'BTCUSDT': KLineDB(fp_p('data', 'BTCUSDT', 'P.db')),
    'SOLUSDT': KLineDB(fp_p('data', 'SOLUSDT', 'P.db')),
}

def _init_db():
    # 初始化数据库
    for symbol, db in symbols.items():
        if db.latest():
            continue
        now = get_time()
        bars = get_klines(symbol)
        for bar in bars:
            if bar[6] - now > 0: # 不完整的k线
                continue
            k = binance_p(bar)
            db.insert(k, False)
            print(symbol, k)
        db.commit()
_init_db()

def _update_db():
    # 更新数据库
    now = get_time()
    res = {}
    for symbol, db in symbols.items():
        bar = db.latest()[0]
        # 一分钟k线
        bars = get_klines(symbol, start_time=bar.ts + 1)
        for bar in bars:
            k = binance_p(bar)
            if bar[6] - now > 0:  # 不完整的k线
                res[symbol] = k
                break
            db.insert(k, False)
        else:
            res[symbol] = db.latest()[0]
        db.commit()
    return res