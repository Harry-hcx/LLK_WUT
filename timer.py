import pygame as pg

font_name = pg.font.match_font("simhei")


class Timer:
    def __init__(self, x=600, y=500):
        self.m = 0
        self.s = 0
        self.ms = 0.0
        self.tick = 0
        self.x = x
        self.y = y
        self.font_size = 30

    def calc(self):
        self.s += self.ms // 1000
        self.ms %= 1000
        self.m += self.s // 60
        self.s %= 60

    def go(self, x):
        self.tick += 1
        self.ms += 0.304 * x
        self.calc()
        print(self.toString(), self.tick)

    def toString(self):
        return str(int(self.m)) + ":" + str(int(self.s)) + "." + str(int(self.ms))

    def draw(self, surface):
        font = pg.font.Font(font_name, self.font_size)
        text = font.render(self.toString(), True, (0, 0, 0))
        surface.blit(text, (self.x, self.y))
