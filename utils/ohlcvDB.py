import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime

class Kline:
    def __init__(self, ts: int, o: float, h: float, l: float, c: float, v: float, taker: float, trades: int):
        self.ts = ts
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        self.v = v
        self.taker = taker
        self.trades = trades
    def __str__(self):
        return f'{ts2ft(self.ts)} O {self.o} H {self.h} L {self.l} C {self.c} V {self.v}'
    __repr__ = __str__

def binance_p(kl):
    return Kline(
        kl[0],
        float(kl[1]),
        float(kl[2]),
        float(kl[3]),
        float(kl[4]),
        float(kl[7]),
        float(kl[10]),
        kl[8]
    )

def cur_p(bars):
    return [Kline(*bar) for bar in bars]

def ts2ft(ts):
    dt_utc = datetime.fromtimestamp(ts / 1000)
    ft = dt_utc.strftime('%Y-%m-%d %H:%M:%S')
    return ft

def ft2ts(ft):
    """%Y-%m-%d %H:%M:%S 格式的时间转换到时间戳"""
    dt_utc = datetime.strptime(ft, '%Y-%m-%d %H:%M:%S')
    return int(dt_utc.timestamp() * 1000)

class KLineDB:
    def __init__(self, db_path: str = "kline.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_table()

    def _init_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS kline (
            ts INTEGER PRIMARY KEY,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            taker REAL,
            trades INTEGER
        )
        """)
        self.conn.commit()

    def insert(self, bar, commit=True):
        """插入一条 K 线（不会更新已有数据，失败抛异常）"""
        try:
            self.conn.execute(
                "INSERT INTO kline (ts, open, high, low, close, volume, taker, trades) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (bar.ts, bar.o, bar.h, bar.l, bar.c, bar.v, bar.taker, bar.trades)
            )
            if commit: self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # 已存在相同 ts 就忽略（因为规则是无删改）

    def commit(self):
        self.conn.commit()

    def query_range(self, ts_start: int, ts_end: int) -> List[Kline]:
        """按时间范围查询"""
        cur = self.conn.execute(
            "SELECT ts, open, high, low, close, volume, taker, trades FROM kline WHERE ts BETWEEN ? AND ? ORDER BY ts ASC",
            (ts_start, ts_end)
        )
        return cur_p(cur.fetchall())

    def latest(self, limit: int = 1) -> List[Kline]:
        """获取最新的 N 条 K线"""
        cur = self.conn.execute(
            "SELECT ts, open, high, low, close, volume, taker, trades FROM kline ORDER BY ts DESC LIMIT ?",
            (limit,)
        )
        return cur_p(cur.fetchall())

    def earliest(self, limit: int = 1) -> List[Kline]:
        """获取最早的 N 条 K线"""
        cur = self.conn.execute(
            "SELECT ts, open, high, low, close, volume, taker, trades FROM kline ORDER BY ts ASC LIMIT ?",
            (limit,)
        )
        return cur_p(cur.fetchall())

    def latest_1h(self, limit: int = 1) -> List[Kline]:
        ts_end = self.latest()[0].ts // 1000 // 3600 * 3600 * 1000 - 1
        ts_start = ts_end - 3600 * 1000 * limit
        return convert_1m_to_1h(self.query_range(ts_start, ts_end))

def convert_1m_to_1h(bars_1m: List[Kline]) -> List[Kline]:
    if not bars_1m:
        return []

    # 按时间排序
    bars_1m.sort(key=lambda x: x.ts)

    result = []

    # 找到第一个整点时间
    first_ts = bars_1m[0].ts
    # 毫秒转小时整点
    first_hour_ts = first_ts - (first_ts % (3600 * 1000))
    # 如果第一个bar的时间不是整点，跳到下一个整点
    if first_ts != first_hour_ts:
        first_hour_ts += 3600 * 1000

    hour_ms = 3600 * 1000

    # 初始化指针
    i = 0
    n = len(bars_1m)

    # 跳过第一个整点前的数据
    while i < n and bars_1m[i].ts < first_hour_ts:
        i += 1

    while i < n:
        hour_start_ts = bars_1m[i].ts
        # 对齐到整点
        hour_start_ts = hour_start_ts - (hour_start_ts % hour_ms)

        hour_end_ts = hour_start_ts + hour_ms

        # 如果数据不足一小时则舍弃
        if bars_1m[-1].ts < hour_end_ts - 60_000:  # 最后一根分钟K时间 < 该小时最后一分钟
            break

        # 收集该小时内的分钟K
        hour_bars = []
        while i < n and bars_1m[i].ts < hour_end_ts:
            hour_bars.append(bars_1m[i])
            i += 1

        o = hour_bars[0].o
        h = max(b.h for b in hour_bars)
        l = min(b.l for b in hour_bars)
        c = hour_bars[-1].c
        v = sum(b.v for b in hour_bars)
        taker = sum(b.taker for b in hour_bars)
        trades = sum(b.trades for b in hour_bars)

        result.append(Kline(hour_start_ts, o, h, l, c, v, taker, trades))

    return result