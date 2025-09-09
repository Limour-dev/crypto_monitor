# ====== 环境配置 ======
import sys, os
fp_root = os.path.dirname(os.path.dirname(__file__))
if fp_root not in sys.path:
    sys.path.append(fp_root)

from utils.logger import fp_p
from utils.ohlcvDB import KLineDB
kdb = KLineDB(fp_p('data', 'ETHUSDT', 'P.db'))
# ====== 计算 ======
# 需要先执行 test/getMoreData.py 获取足够的数据
bars = kdb.latest(60 * 24)
p_min = float('inf')
p_max = float('-inf')
for bar in bars:
    bar.hlc3 = (bar.h + bar.l + bar.c) / 3
    bar.maker = bar.v - bar.taker
    bar.t_q = bar.taker / bar.hlc3
    bar.m_q = bar.maker / bar.hlc3
    p_min = min(p_min, bar.hlc3)
    p_max = max(p_max, bar.hlc3)

p_rs = 30
p_rg = p_max - p_min

p_buy = [0] * p_rs
p_sell = [0] * p_rs

p_fc = 1 / p_rg * p_rs
for bar in bars:
    p_c = (bar.hlc3 - p_min) * p_fc
    p_a = max(min(int(p_c), p_rs - 1), 0)
    p_buy[p_a] += bar.t_q
    p_sell[p_a] += bar.m_q

res = []
p_fc = 1 / p_rs * p_rg
for i in range(p_rs):
    res.append(f'{p_min + i * p_fc:.2f}\t{p_buy[i]}\t{p_sell[i]}')
tmp = '\n'.join(res)