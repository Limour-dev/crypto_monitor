from notify.wechat_bot import wechat_push
from strategy.common import macd, ta_stdev

key_levels_last_notify = 0
notify_interval = 59999
last_c_1h = 0

def p_bar(bar, symbols):
    global key_levels_last_notify, last_c_1h
    bars_1h = symbols['ETHUSDT'].latest_1h(400)
    if bars_1h[-1].ts > last_c_1h:
        last_c_1h = bars_1h[-1].ts
        src = [k.c for k in bars_1h]
        macd_line = macd(src)[-200:]
        middle = macd_line[-1] - sum(macd_line) / 200
        stdev = ta_stdev(macd_line)
        if middle > stdev:
            wechat_push(f'ETHUSDT up {bar.c:.2f}')
        elif middle < -stdev:
            wechat_push(f'ETHUSDT down {bar.c:.2f}')