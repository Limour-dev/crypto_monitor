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