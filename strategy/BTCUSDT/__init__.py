from notify.wechat_bot import wechat_push
from strategy.common import crossover, buy_vs_sell
from strategy.common import f_log_regression, ta_stdev
from itertools import chain

key_levels = []

key_levels_last_notify = 0
notify_interval = 59999

lg_last_c = 0
lg = [0, 0]

def p_bar(bar, symbols):
    global key_levels_last_notify, lg_last_c
    global lg
    bars_1h = symbols['BTCUSDT'].latest_1h(150)
    if bars_1h[-1].ts > lg_last_c:
        lg_last_c = bars_1h[-1].ts
        src = [k.c for k in bars_1h[::-1]]

        middle = f_log_regression(src)[1]
        st_dev = ta_stdev(src)
        lg[0] = middle + 1.5 * st_dev
        lg[1] = middle - 1.5 * st_dev

        wechat_push(f'BTCUSDT\n {buy_vs_sell(bars_1h)}')

    for level in chain(key_levels, lg):
        # print(level)
        tmp = crossover(bar, level)
        if tmp:
            if bar.ts - key_levels_last_notify >= notify_interval:
                wechat_push(f'BTCUSDT {level:.2f} {tmp} \n {bar}')
                key_levels_last_notify = bar.ts