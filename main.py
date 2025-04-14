import pygame as pg
import sys
import random
import time
from button import *
from block import *
from timer import *
from hintline import *

WIDTH = 800
HEIGHT = 600
TYPE = 10


def generate_map(n, m):
    s = []
    while len(s) < n * m:
        for i in range(TYPE):
            s.append(str(i))
            s.append(str(i))
            if len(s) >= n * m:
                break

    random.shuffle(s)
    return "".join(s)


def check(x1, y1, x2, y2, vis):
    print("checking", x1, y1, x2, y2, vis)
    ox1 = x1
    oy1 = y1
    ox2 = x2
    oy2 = y2
    n = len(vis)
    m = len(vis[0])
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    map1 = []
    map2 = []
    sumx = [[0 for j in range(m + 1)] for i in range(n + 1)]
    sumy = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if i < n and j < m:
                sumx[i][j] = vis[i][j]
                sumy[i][j] = vis[i][j]
            if i == 0:
                sumx[i][j] += sumx[i][j - 1]
            elif j == 0:
                sumy[i][j] += sumy[i - 1][j]
            else:
                sumy[i][j] += sumy[i - 1][j]
                sumx[i][j] += sumx[i][j - 1]
    if abs(x1 - x2) + abs(y1 - y2) == 1:
        return [
            True,
            (oy1 * 40 + 70, ox1 * 40 + 70),
            (y1 * 40 + 70, x1 * 40 + 70),
            (y2 * 40 + 70, x2 * 40 + 70),
            (oy2 * 40 + 70, ox2 * 40 + 70),
        ]
    for dir in range(4):
        nx = x1 + dx[dir]
        ny = y1 + dy[dir]
        while nx >= -1 and nx <= n and ny >= -1 and ny <= m:
            if nx >= 0 and nx < n and ny >= 0 and ny < m and vis[nx][ny] == 1:
                break
            map1.append((nx, ny))
            nx += dx[dir]
            ny += dy[dir]

    for dir in range(4):
        nx = x2 + dx[dir]
        ny = y2 + dy[dir]
        while nx >= -1 and nx <= n and ny >= -1 and ny <= m:
            if nx >= 0 and nx < n and ny >= 0 and ny < m and vis[nx][ny] == 1:
                break
            map2.append((nx, ny))
            print(nx, ny)
            nx += dx[dir]
            ny += dy[dir]
    for x1, y1 in map1:
        for x2, y2 in map2:
            print(x1, y1, x2, y2, sep=" ")
            if x1 == x2 == -1 or x1 == x2 == n or y1 == y2 == -1 or y1 == y2 == m:
                return [
                    True,
                    (oy1 * 40 + 70, ox1 * 40 + 70),
                    (y1 * 40 + 70, x1 * 40 + 70),
                    (y2 * 40 + 70, x2 * 40 + 70),
                    (oy2 * 40 + 70, ox2 * 40 + 70),
                ]
            if (x1 == x2) and (
                sumx[x1][max(y1, y2)] - sumx[x1][min(y1, y2)] + vis[x1][min(y1, y2)]
                == 0
            ):
                return [
                    True,
                    (oy1 * 40 + 70, ox1 * 40 + 70),
                    (y1 * 40 + 70, x1 * 40 + 70),
                    (y2 * 40 + 70, x2 * 40 + 70),
                    (oy2 * 40 + 70, ox2 * 40 + 70),
                ]
            if (y1 == y2) and (
                sumy[max(x1, x2)][y1] - sumy[min(x1, x2)][y1] + vis[min(x1, x2)][y1]
                == 0
            ):
                return [
                    True,
                    (oy1 * 40 + 70, ox1 * 40 + 70),
                    (y1 * 40 + 70, x1 * 40 + 70),
                    (y2 * 40 + 70, x2 * 40 + 70),
                    (oy2 * 40 + 70, ox2 * 40 + 70),
                ]

    return [False, (-1, -1), (-1, -1)]


def find_hint(vis, level):
    n = len(vis)
    m = len(vis[0])
    possible_blocks = []
    for i in range(n):
        for j in range(m):
            if vis[i][j] == 0:
                continue
            for x in range(i, n):
                for y in range(j, m):
                    if i == x and j == y:
                        continue
                    if vis[x][y] == 0:
                        continue
                    if level[i][j].type == level[x][y].type:
                        temp = check(i, j, x, y, vis)
                        if temp[0]:
                            print(i, j, x, y, temp)
                            return temp


def play(screen, level_data, width=16, height=10, goal=-1, is_relax=False):
    width = min(width, 16)
    height = min(height, 10)
    level_data = generate_map(width, height)
    running = True
    level = []
    visit = [[False for i in range(width)] for i in range(height)]
    clock = pg.time.Clock()
    ready = True
    deleted = 0
    hintline = HintLine()
    for i in range(height):
        temp = []
        for j in range(width):
            temp.append(Block(level_data[i * width + j], 50 + j * 40, 50 + i * 40))
        level.append(temp)
    timer = Timer()
    goal_time = Timer(start=goal)
    print(goal_time.toString())
    while running:
        screen.fill((0, 0, 0))
        bg = pg.image.load("assets/fruit_bg.bmp")
        screen.blit(bg, (0, 0))
        button_start = Button(700, 50, text="开始游戏")
        button_pause = Button(700, 150, text="暂停游戏")
        button_hint = Button(700, 250, text="提示")
        button_rearrange = Button(700, 350, text="重排")
        button_exit = Button(700, 450, bg_color=(255, 0, 0), text="退出")
        if goal != -1:
            button_goal = Button(
                600, 550, bg_color=(13, 123, 13), text=(goal_time.toString())
            )
            button_goal.draw(screen)
        button_start.draw(screen)
        button_pause.draw(screen)
        button_hint.draw(screen)
        button_rearrange.draw(screen)
        button_exit.draw(screen)
        # print(ready)
        events = pg.event.get()
        hintline.draw(screen)
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if button_start.is_clicked(event):
                ready = False
            if button_exit.is_clicked(event):
                return
            if button_pause.is_clicked(event):
                ready = not ready
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    ready = not ready

        if ready:
            lock = pg.image.load("assets/lock.png")
            screen.blit(lock, (100, 100))
            pg.display.flip()
            continue

        timer.go(60)
        for i in range(height):
            for j in range(width):
                level[i][j].draw(screen)
        if not is_relax:
            timer.draw(screen)
        pg.display.flip()
        clock.tick(60)
        for event in events:
            for i in range(height):
                for j in range(width):
                    if level[i][j].is_visible == False:
                        continue
                    if level[i][j].is_clicked(event):
                        level[i][j].is_chosen = not level[i][j].is_chosen
            if button_rearrange.is_clicked(event):
                print("rearrange")
                level_data = generate_map(width, height)
                level = []
                deleted = 0
                for i in range(height):
                    temp = []
                    for j in range(width):
                        temp.append(
                            Block(level_data[i * width + j], 50 + j * 40, 50 + i * 40)
                        )
                    level.append(temp)
            if button_hint.is_clicked(event):
                print("hint")
                answer = find_hint(
                    [
                        [int(level[i][j].is_visible) for j in range(width)]
                        for i in range(height)
                    ],
                    level,
                )
                try:
                    hintline.update(answer[1:])
                except:
                    hintline.update(
                        [(700, 350), (700, 400), (790, 400), (790, 350), (700, 350)]
                    )

        chosen = []
        for i in range(height):
            for j in range(width):
                if level[i][j].is_chosen and level[i][j].is_visible:
                    chosen.append((i, j))
        if len(chosen) == 2:
            if (
                check(
                    chosen[0][0],
                    chosen[0][1],
                    chosen[1][0],
                    chosen[1][1],
                    [
                        [int(level[i][j].is_visible) for j in range(width)]
                        for i in range(height)
                    ],
                )[0]
                and level[chosen[0][0]][chosen[0][1]].type
                == level[chosen[1][0]][chosen[1][1]].type
            ):
                level[chosen[0][0]][chosen[0][1]].set_invisible()
                level[chosen[1][0]][chosen[1][1]].set_invisible()
                deleted += 2
                hintline.dead()
            else:
                level[chosen[0][0]][chosen[0][1]].is_chosen = False
                level[chosen[1][0]][chosen[1][1]].is_chosen = False
        if deleted == width * height:
            congrate_button = Button(
                200, 150, 400, 300, (255, 255, 255), "恭喜过关", 90
            )
            congrate_button.draw(screen)
            pg.display.flip()
            time.sleep(3)
            running = False
    print(timer.tick)
    return timer.tick


def chose_level(screen):

    running = True
    while running:
        level_num = 0
        width = []
        height = []
        data = []
        level = []
        limit = []
        screen.fill((0, 0, 0))
        bg = pg.image.load("assets/level_bg.png")
        screen.blit(bg, (0, 0))
        for i in range(99):
            try:
                with open("levels/" + str(i + 1) + ".txt", "r") as f:
                    width.append(int(f.readline()[:-1]))
                    height.append(int(f.readline()[:-1]))
                    data.append(f.readline()[:-1])
                    limit.append(int(f.readline()))
                level_num += 1
            except:
                break
        # print("Detected ", level_num, " levels")
        accepted = []
        try:
            with open("levels/rec.txt", "r") as f:
                temp = f.readline()
                for c in temp:
                    accepted.append(int(c))
        except:
            with open("levels/rec.txt", "w") as f:
                f.write("".join(accepted))
        while len(accepted) < level_num:
            accepted.append(0)
        column = 0
        button_back = Button(600, 500, text="返回", font_size=35)
        button_back.draw(screen)
        for i in range(level_num):
            row = i % 8
            level.append(
                Button(
                    50 + row * 80,
                    50 + column * 80,
                    60,
                    60,
                    [(255, 250, 240), (0, 205, 102), (238, 59, 59)][accepted[i]],
                    str(i + 1),
                    45,
                )
            )
            level[i].draw(screen)
            if i % 8 == 7:
                column += 1
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if button_back.is_clicked(event):
                running = False
            for i in range(level_num):
                if level[i].is_clicked(event):
                    if play(screen, data[i], width[i], height[i], limit[i]) > limit[i]:
                        accepted[i] = 2
                    else:
                        accepted[i] = 1
                    print(limit[i])
        with open("levels/rec.txt", "w") as f:
            f.write("".join([str(i) for i in accepted]))


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF)
    pg.display.set_caption("连连看")
    icon = pg.image.load("assets/LLK.ico").convert_alpha()
    pg.display.set_icon(icon)

    clock = pg.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))
        bg = pg.image.load("assets/llk_main.bmp")
        screen.blit(bg, (0, 0))
        button_basic = Button(29, 222, text="基本模式")
        button_relax = Button(29, 333, text="休闲模式")
        button_level = Button(29, 444, text="关卡模式")
        button_rank = Button(507, 545, text="排行榜")
        button_setting = Button(607, 545, text="设置")
        button_help = Button(707, 545, text="帮助")
        button_basic.draw(screen)
        button_relax.draw(screen)
        button_level.draw(screen)
        button_rank.draw(screen)
        button_setting.draw(screen)
        button_help.draw(screen)

        clock.tick(30)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if button_basic.is_clicked(event):
                random_width = 4
                random_height = 4
                random_str = generate_map(random_width, random_height)
                play(screen, random_str, width=random_width, height=random_height)
            if button_level.is_clicked(event):
                chose_level(screen)
            if button_relax.is_clicked(event):
                random_width = 4
                random_height = 4
                random_str = generate_map(random_width, random_height)
                play(
                    screen,
                    random_str,
                    width=random_width,
                    height=random_height,
                    is_relax=True,
                )


if __name__ == "__main__":
    main()
