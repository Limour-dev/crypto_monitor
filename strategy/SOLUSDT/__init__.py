from notify.wechat_bot import wechat_push
from strategy.common import macd, ta_stdev

key_levels_last_notify = 0
notify_interval = 59999
last_c_1h = 0

nt_macd_up = False
nt_macd_down = False

def p_bar(bar, symbols):
    global key_levels_last_notify, last_c_1h
    global nt_macd_up, nt_macd_down
    bars_1h = symbols['SOLUSDT'].latest_1h(400)
    if bars_1h[-1].ts > last_c_1h:
        last_c_1h = bars_1h[-1].ts
        src = [k.c for k in bars_1h]
        macd_line = macd(src)[-200:]
        middle = macd_line[-1] - sum(macd_line) / 200
        stdev = ta_stdev(macd_line)
        if middle >= stdev:
            if nt_macd_up:
                pass
            else:
                wechat_push(f'SOLUSDT up {bar.c:.2f}')
                nt_macd_up = True
        elif middle <= -stdev:
            if nt_macd_down:
                pass
            else:
                wechat_push(f'SOLUSDT down {bar.c:.2f}')
                nt_macd_down = True
        else:
            if nt_macd_up:
                wechat_push(f'SOLUSDT not up {bar.c:.2f}')
                nt_macd_up = False
            if nt_macd_down:
                wechat_push(f'SOLUSDT not down {bar.c:.2f}')
                nt_macd_down = False