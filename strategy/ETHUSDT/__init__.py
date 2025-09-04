from notify.wechat_bot import wechat_push
from strategy.common import crossover

key_levels = [
    4117, 4215, 4262, 4306, 4349, 4387, 4453, 4496
]

key_levels_last_notify = 0
notify_interval = 59999

def p_bar(bar, symbols):
    global key_levels_last_notify
    for level in key_levels:
        tmp = crossover(bar, level)
        if tmp:
            if bar.ts - key_levels_last_notify >= notify_interval:
                wechat_push(f'ETHUSDT {bar} crossover {level} {tmp}')
                key_levels_last_notify = bar.ts