import pygame
from pygame.locals import *

# 初始化Pygame
pygame.init()

# 创建第一个窗口
window1 = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Window 1")

# 创建第二个窗口
window2 = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Window 2")

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # 在每个窗口上绘制内容
    window1.fill((255, 255, 255))
    window2.fill((0, 0, 0))

    pygame.display.update()

# 退出Pygame
pygame.quit()
