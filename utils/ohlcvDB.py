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
