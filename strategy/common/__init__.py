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