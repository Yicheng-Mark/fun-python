import tkinter as tk
import random
import time

# --- 优化后的配置参数 ---
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800
PARTICLE_COUNT = 150
EXPLOSION_SPEED = 5.0
ROCKET_LIFT_SPEED = -20  # **更快上升**
GRAVITY = 0.1           # **粒子下落更慢，飞行更远**
DELAY = 0.01             # **更新频率更高，动画更流畅/快速**
FIREWORK_COLORS = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#00FFFF', '#FF00FF', '#FFFFFF', '#00BFFF', '#FF1493']
ROCKET_LAUNCH_INTERVAL = 1800 # **更快连续发射**


# -----------------------------------------------------------
# 1. Particle 类 (与上次基本相同，用于爆炸后的粒子)
# -----------------------------------------------------------

class Particle:
    """单个烟花粒子"""

    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color

        # 随机分配初始速度
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(EXPLOSION_SPEED / 2, EXPLOSION_SPEED)

        # 增加一些扩散时的随机性
        self.vx = speed * (random.random() * 2 - 1)
        self.vy = speed * (random.random() * 2 - 1)

        self.life = random.uniform(20, 50)
        self.radius = 2

        self.shape = canvas.create_oval(
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius,
            fill=color, outline=color
        )

    def update(self):
        """更新粒子的位置和状态"""
        # 应用重力
        self.vy += GRAVITY

        # 更新位置
        self.x += self.vx
        self.y += self.vy

        # 衰减生命值
        self.life -= 1

        # 移动粒子
        self.canvas.coords(
            self.shape,
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius
        )

        # 缩小粒子半径
        if self.life < 10:
            self.radius = max(0, self.radius - 0.2)

        return self.life > 0

    def delete(self):
        """从画布上删除粒子"""
        self.canvas.delete(self.shape)


# -----------------------------------------------------------
# 2. Rocket 类 (新的类，用于上升阶段)
# -----------------------------------------------------------

class Rocket:
    """烟花火箭，负责从地面上升并爆炸"""

    def __init__(self, canvas, start_x):
        self.canvas = canvas
        self.x = start_x
        self.y = CANVAS_HEIGHT  # 从底部开始
        self.vy = ROCKET_LIFT_SPEED
        self.color = random.choice(FIREWORK_COLORS)
        self.radius = 3

        # 火箭上升过程的“尾迹”颜色，通常较暗
        self.tail_color = '#555555'

        # 创建火箭形状
        self.shape = canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=self.tail_color, outline=self.tail_color
        )

        # 爆炸高度随机化
        self.max_height = random.uniform(CANVAS_HEIGHT / 3, CANVAS_HEIGHT * 2 / 3)

    def update(self):
        """更新火箭位置，并检查是否爆炸"""

        # 1. 模拟上升速度减缓 (空气阻力或燃料耗尽)
        if self.vy < 0:
            self.vy += 0.08

        self.y += self.vy

        # 2. 移动火箭
        self.canvas.coords(
            self.shape,
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius
        )

        # 3. 检查是否达到爆炸高度 (上升速度变为正或达到随机高度)
        # 当速度开始下降（vy > 0 意味着开始下落）时爆炸，或达到预设高度
        should_explode = self.vy >= 0 or self.y < self.max_height

        if should_explode:
            self.delete()  # 删除火箭形状
            return True  # 返回 True 表示需要爆炸

        return False  # 仍在上升

    def delete(self):
        """从画布上删除火箭形状"""
        self.canvas.delete(self.shape)


# -----------------------------------------------------------
# 3. FireworkApp 类 (主程序逻辑)
# -----------------------------------------------------------

class FireworkApp:
    """烟花应用主类"""

    def __init__(self, master):
        self.master = master
        master.title("Python 自动烟花模拟 🎇")

        self.canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black')
        self.canvas.pack()

        self.particles = []  # 存储爆炸后的粒子
        self.rockets = []  # 存储正在上升的火箭

        self.is_running = True

        # 自动发射第一个烟花
        self.launch_new_rocket()

        # 开始动画循环
        self.update_animation()

    def launch_new_rocket(self):
        """创建并发射一个新的火箭"""
        start_x = random.randint(50, CANVAS_WIDTH - 50)
        r = Rocket(self.canvas, start_x)
        self.rockets.append(r)

        # 设置定时器，自动发射下一个
        self.master.after(ROCKET_LAUNCH_INTERVAL, self.launch_new_rocket)

    def create_explosion(self, x, y, color):
        """在指定位置创建爆炸效果"""
        for _ in range(PARTICLE_COUNT):
            p = Particle(self.canvas, x, y, color)
            self.particles.append(p)

    def update_animation(self):
        """主动画循环：更新粒子和火箭"""
        if not self.is_running:
            return

        # --- 1. 更新火箭 ---
        rockets_to_keep = []
        for r in self.rockets:
            if r.update():
                # 火箭爆炸
                self.create_explosion(r.x, r.y, r.color)
            else:
                rockets_to_keep.append(r)

        self.rockets = rockets_to_keep

        # --- 2. 更新粒子 ---
        particles_to_keep = []
        particles_to_delete = []

        for p in self.particles:
            if p.update():
                particles_to_keep.append(p)
            else:
                particles_to_delete.append(p)

        for p in particles_to_delete:
            p.delete()

        self.particles = particles_to_keep

        # 递归调用自身，保持动画流畅
        self.master.after(int(DELAY * 1000), self.update_animation)


# --- 运行程序 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FireworkApp(root)
    root.mainloop()