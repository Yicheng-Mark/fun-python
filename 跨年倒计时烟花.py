import pygame
import sys
import random
import math
import datetime

# 初始化pygame
pygame.init()

# 设置屏幕大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("祝你新年快乐")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 字体 - 使用支持中文的字体列表，提供备选以提高兼容性
# 【原代码已删除】

# ==================== 【最小修复 - 只改这里】 ====================
pygame.font.init()  # 强制初始化字体（解决注册表bug）

font_large = None
font_medium = None

# 直接从Windows字体文件加载（绕过SysFont崩溃）
font_paths = [
    r"C:\Windows\Fonts\msyh.ttc",      # 微软雅黑
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf"
]

for path in font_paths:
    try:
        font_large = pygame.font.Font(path, 100)
        font_medium = pygame.font.Font(path, 50)
        print(f"✅ 成功加载字体: {path}")
        break
    except:
        continue

# 如果都没找到，使用保底字体（不会崩溃）
if font_large is None:
    print("⚠️ 使用Pygame默认字体（中文可能方块）")
    font_large = pygame.font.Font(None, 100)
    font_medium = pygame.font.Font(None, 50)
# ==================== 【修复结束】 ====================

# 目标时间：自动指向下一个新年（每年1月1日0点），无需手动修改，永远有效
# 为测试可临时改为：target_time = datetime.datetime.now() + datetime.timedelta(seconds=10)
now = datetime.datetime.now()
target_time = datetime.datetime(now.year + 1, 1, 1, 0, 0, 0)

# 创建烟花层表面
fireworks_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# 烟花类
class Firework:
    def __init__(self):
        self.particles = []
        self.launching = True
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.speed = random.uniform(5, 10)
        self.explosion_height = random.randint(100, HEIGHT // 2)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.exploded = False
        self.fade_time = 0

    def update(self):
        if self.launching:
            self.y -= self.speed
            if self.y <= self.explosion_height:
                self.launching = False
                self.exploded = True
                self.explode()
        elif self.exploded:
            new_particles = []
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.1  # 重力
                p['life'] -= 1
                p['alpha'] = max(0, p['life'] / p['max_life'] * 255)
                if p['life'] > 0:
                    new_particles.append(p)
            self.particles = new_particles
            if not self.particles:
                self.fade_time += 1
                if self.fade_time > 60:  # 消失后等待一段时间
                    self.__init__()  # 重置烟花

    def explode(self):
        num_particles = random.randint(50, 100)
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - random.uniform(2, 4)  # 初始向上力
            life = random.randint(50, 100)
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': vx,
                'vy': vy,
                'life': life,
                'max_life': life,
                'color': self.color,
                'alpha': 255
            })

    def draw(self, surface):
        if self.launching:
            pygame.draw.line(surface, self.color, (self.x, HEIGHT), (self.x, self.y), 3)
        elif self.exploded:
            for p in self.particles:
                color = (*p['color'], int(p['alpha']))
                pygame.draw.circle(surface, color, (int(p['x']), int(p['y'])), 2)

# 闪光粒子类
class Sparkle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        self.life = random.randint(20, 60)
        self.max_life = self.life
        self.size = random.uniform(1, 3)

    def update(self):
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = (self.life / self.max_life) * 255
        color = (*self.color, int(alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))

# 创建多个烟花
fireworks = [Firework() for _ in range(5)]

# 闪光列表
sparkles = []

# 主循环
clock = pygame.time.Clock()
running = True
countdown_ended = False

# 彩虹颜色列表
rainbow_colors = [
    (255, 0, 0),    # 红
    (255, 165, 0),  # 橙
    (255, 255, 0),  # 黄
    (0, 255, 0),    # 绿
    (0, 0, 255),    # 蓝
    (75, 0, 130),   # 靛
    (238, 130, 238) # 紫
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # 计算倒计时
    now = datetime.datetime.now()
    delta = target_time - now
    if delta.total_seconds() <= 0:
        if not countdown_ended:
            countdown_ended = True
            # 初始化闪光
            sparkles = []
        days, hours, minutes, seconds = 0, 0, 0, 0
    else:
        countdown_ended = False
        days = delta.days
        seconds = int(delta.total_seconds()) % 60
        minutes = (int(delta.total_seconds()) // 60) % 60
        hours = (int(delta.total_seconds()) // 3600) % 24

    if not countdown_ended:
        # 显示倒计时
        countdown_text = f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
        text_surf = font_large.render(countdown_text, True, WHITE)
        shadow_surf = font_large.render(countdown_text, True, (255, 255, 0))  # 发光阴影（黄色）
        glow_surf = pygame.Surface((text_surf.get_width() + 10, text_surf.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (255, 255, 0, 50), (0, 0, glow_surf.get_width(), glow_surf.get_height()))
        glow_surf.blit(shadow_surf, (5, 5))
        screen.blit(glow_surf, (WIDTH // 2 - text_surf.get_width() // 2 - 5, HEIGHT // 2 - text_surf.get_height() // 2 - 5))
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, HEIGHT // 2 - text_surf.get_height() // 2))
    else:
        # 显示"新年快乐!" 以彩虹颜色和闪光效果
        happy_text = (" 2026新年快乐 ")
        x_pos = WIDTH // 2
        y_pos = HEIGHT // 2
        total_width = 0
        char_surfs = []
        for i, char in enumerate(happy_text):
            color = rainbow_colors[i % len(rainbow_colors)]
            char_surf = font_medium.render(char, True, color)
            char_surfs.append((char_surf, color, char))
            total_width += char_surf.get_width()

        current_x = x_pos - total_width // 2
        for char_surf, color, char in char_surfs:
            # 添加阴影
            shadow_surf = font_medium.render(char, True, (min(color[0]+50,255), min(color[1]+50,255), min(color[2]+50,255)))
            screen.blit(shadow_surf, (current_x + 2, y_pos + 2))
            screen.blit(char_surf, (current_x, y_pos))
            current_x += char_surf.get_width()

        # 更新和绘制闪光
        new_sparkles = []
        for s in sparkles:
            if s.update():
                s.draw(screen)
                new_sparkles.append(s)
        sparkles = new_sparkles

        # 随机添加新闪光
        if random.random() < 0.3:  # 控制闪光密度
            sparkle_x = random.randint(x_pos - total_width // 2, x_pos + total_width // 2)
            sparkle_y = random.randint(y_pos - 20, y_pos + font_medium.get_height() + 20)
            sparkles.append(Sparkle(sparkle_x, sparkle_y))

        # 更新烟花
        for fw in fireworks:
            fw.update()

        # 清空烟花表面
        fireworks_surface.fill((0, 0, 0, 0))

        # 绘制所有烟花到烟花表面
        for fw in fireworks:
            fw.draw(fireworks_surface)

        # 将烟花表面blit到屏幕
        screen.blit(fireworks_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()