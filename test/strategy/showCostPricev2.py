# ====== 绘图函数 ======
import tkinter as tk

root = tk.Tk()
width, height = 1500, 600
margin = 50  # 留出空间显示坐标
canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.pack()

axes_drawn = False

def plot_line_with_axes(data, min_val, max_val, color='blue'):
    global axes_drawn
    span_y = max_val - min_val if max_val > min_val else 1

    # 缩放函数
    def scale_x(val):
        return margin + val * (width - 2 * margin) / (len(data) - 1)

    def scale_y(val):
        return height - margin - (val - min_val) / span_y * (height - 2 * margin)

    # 只在第一次调用时画坐标轴
    if not axes_drawn:
        # 画坐标轴
        canvas.create_line(margin, margin, margin, height - margin, width=2)  # Y轴
        canvas.create_line(margin, height - margin, width - margin, height - margin, width=2)  # X轴

        # 画刻度 - Y 轴
        y_steps = 5  # Y轴分成几段
        for i in range(y_steps + 1):
            y_val = min_val + i * span_y / y_steps
            y_pos = scale_y(y_val)
            canvas.create_line(margin - 5, y_pos, margin + 5, y_pos)  # 刻度线
            canvas.create_text(margin - 10, y_pos, angle=45, text=f"{y_val:.1f}", anchor="e")  # 刻度值

        # 画刻度 - X 轴
        for i, v in enumerate(data):
            j = i - len(data)
            if j % x_it != 0:
                continue
            x_pos = scale_x(i)
            canvas.create_line(x_pos, height - margin - 5, x_pos, height - margin + 5)  # 刻度线
            canvas.create_text(x_pos, height - margin + 15, angle=45, text=str(j // x_it), anchor="n")  # 刻度值（用索引）

        axes_drawn = True

    # 画折线
    coords = []
    for i, v in enumerate(data):
        coords.append(scale_x(i))
        coords.append(scale_y(v))
    canvas.create_line(coords, fill=color, width=2)

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
period = 1
x_it = max(60 // period, 1)
lw = 30
bars = kdb.latest(60 * 12 + lw)[::-1]

root.title(f"买卖量比例")

for bar in bars:
    bar.maker = bar.v - bar.taker

t_buy_p = sum(x.taker for x in bars[:lw])
t_sell_p = sum(x.maker for x in bars[:lw])

line_sell = []
line_buy = []
for i in range(lw, len(bars)):
    bari = bars[i]
    baro = bars[i-lw]
    t_buy_p += (bari.taker - baro.taker)
    t_sell_p += (bari.maker  - baro.maker)
    line_buy.append(t_buy_p)
    line_sell.append(t_sell_p)

line_sell = line_sell[::-period][::-1]
line_buy = line_buy[::-period][::-1]
line_p = [x.c for x in bars[::-period][:len(line_sell)][::-1]]
line_hist = [(line_sell[i] - line_buy[i])/(line_sell[i] + line_buy[i]) for i in range(len(line_sell))]
# ====== 绘图 ======
_min_val = min(line_p)
_max_val = max(line_p)

plot_line_with_axes(line_p, _min_val, _max_val, color='blue')

h_min = min(line_hist)
h_max = max(line_hist)
plot_line_with_axes(line_hist, h_min, h_max, color='brown')
plot_line_with_axes([min(max(0, h_min), h_max)]*len(line_hist), h_min, h_max, color='yellow')
# ====== 展示 ======
root.mainloop()
