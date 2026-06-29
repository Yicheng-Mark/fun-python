import tkinter as tk
import random
import threading
import time


def show_warn_tip():
    # 创建窗口
    window = tk.Tk()

    # 获取屏幕宽高
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 随机窗口位置(确保窗口完全显示在屏幕内）
    window_width = 250
    window_height = 60
    x = random.randrange(0, screen_width - window_width)
    y = random.randrange(0, screen_height - window_height)

    # 设置窗口标题和大小位置
    window.title('温馨提示')
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 提示文字列表
    tips = ['多喝水', '保持微笑', '天天开心', '天天开心', '事事顺利', '好好爱自己', '多吃蔬菜',
            '梦想成真', '愿所以烦恼都消失', '期待和你见面', '早点睡觉',
            '身体健康', '想我就找我', '早安', '午安', '晚安', '注意休息', '相信自己', '不要生气']

    tip = random.choice(tips)

    # 多样的背景颜色
    bg_colors = ['lightpink', 'skyblue', 'lightgreen', 'lavender', 'lightyellow', 'plum', 'coral', 'bisque',
                 'aquamarine', 'mistyrose', 'honeydew']
    bg = random.choice(bg_colors)

    # 创建标签并显示文字
    tk.Label(window, text=tip, bg=bg, font=('微软雅黑', 16), width=30, height=3).pack()

    # 窗口置顶显示
    window.attributes('-topmost', True)

    # 设置窗口自动关闭时间（5秒后关闭，避免窗口过多无法操作）
    window.after(5000, window.destroy)

    window.mainloop()

if __name__ == "__main__":
    # 创建线程列表
    threads = []
    # 窗口数量（建议不要太多，否则可能导致系统卡顿）
    window_count = 500  # 这里修改为合适的数量

    for i in range(window_count):
        t = threading.Thread(target=show_warn_tip)
        threads.append(t)
        t.start()
        time.sleep(0.09)  # 稍微延长间隔，避免瞬间创建过多窗口导致崩溃