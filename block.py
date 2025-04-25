from button import *


class Block:
    def __init__(self, type, x, y, width=40, height=40):
        self.bg = pg.image.load("assets/split_" + str(type) + ".png")
        self.is_visible = True
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_chosen = False
        self.rect = pg.Rect(x, y, width, height)
        self.type = type

    def draw(self, surface):
        if self.is_visible == False:
            return
        if self.is_chosen:
            pg.draw.rect(surface, (255, 0, 155), self.rect)
        surface.blit(self.bg, (self.x, self.y))

    def set_visible(self):
        self.is_visible = True

    def set_invisible(self):
        self.is_visible = False

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
