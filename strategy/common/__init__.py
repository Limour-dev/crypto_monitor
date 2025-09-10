import math

def crossover(bar, level):
    """
    level: float
    """
    if bar.o < level < bar.c:
        return 'up'
    elif bar.o > level > bar.c:
        return 'down'
    else:
        return None

def f_log_regression(src):
    sumX = 0.0
    sumY = 0.0
    sumXSqr = 0.0
    sumXY = 0.0
    length = len(src)

    for i in range(length):
        val = math.log(src[i])
        per = i + 1.0
        sumX += per
        sumY += val
        sumXSqr += per * per
        sumXY += val * per

    slope = (length * sumXY - sumX * sumY) / (length * sumXSqr - sumX * sumX)
    intercept = (sumY - slope * sumX) / length

    reg_start = math.exp(intercept + slope * length)
    reg_end = math.exp(intercept)

    return reg_start, reg_end, slope

def ta_stdev(src):
    """
    计算 src 最后 length 个元素的样本标准差。
    src: list[float] 或类似序列
    length: 取几根数据
    """
    mean = sum(src) / len(src)
    # 样本标准差 (除以 n-1)
    variance = sum((x - mean) ** 2 for x in src) / (len(src) - 1)
    return math.sqrt(variance)

def buy_vs_sell_v(bar):
    return (bar.taker * 2 - bar.v) / bar.v * 100
def buy_vs_sell_p(bar):
    return (bar.c - bar.o) / bar.c * 1000
def buy_vs_sell(bars):
    res = f'{buy_vs_sell_p(bars[-3]):.2f}\t{buy_vs_sell_v(bars[-3]):.2f}\n'
    res += f'{buy_vs_sell_p(bars[-2]):.2f}\t{buy_vs_sell_v(bars[-2]):.2f}\n'
    res += f'{buy_vs_sell_p(bars[-1]):.2f}\t{buy_vs_sell_v(bars[-1]):.2f}'
    return res

def ema(prices, period):
    """
    计算EMA
    prices: list[float]
    period: int
    """
    ema_values = []
    k = 2 / (period + 1)
    ema_prev = prices[0]  # 第一个EMA起始点可设为首个收盘价
    ema_values.append(ema_prev)

    for price in prices[1:]:
        ema_prev = price * k + ema_prev * (1 - k)
        ema_values.append(ema_prev)

    return ema_values

def sma(prices, period):
    """
    计算简单移动平均 SMA
    """
    wd = sum(prices[:period])
    sma_values = [wd / period]
    for i in range(0, len(prices) - period):
        wd += (prices[i+period] - prices[i])
        sma_values.append(wd / period)
    return sma_values

def macd(prices, fastperiod=12, slowperiod=26):
    """
    纯 Python 实现MACD
    prices: list[float] 收盘价数组
    """

    ema_fast = ema(prices, fastperiod)
    ema_slow = ema(prices, slowperiod)

    # 计算 DIF
    dif = [f - s for f, s in zip(ema_fast, ema_slow)]

    return dif