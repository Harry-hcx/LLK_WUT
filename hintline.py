import pygame as pg


class HintLine:
    def __init__(self):
        self.node = []
        self.ddl = 0

    def update(self, node):
        self.node = node
        self.ddl = 360

    def draw(self, surface):
        if self.ddl <= 0:
            return
        pg.draw.lines(surface, (0, 0, 0), False, self.node, 4)
        self.ddl -= 1
        # print("draw hineline")

    def dead(self):
        self.ddl = 0
