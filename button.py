import pygame as pg

font_name = pg.font.match_font("simhei")


class Button:
    def __init__(
        self, x, y, width=90, height=50, bg_color=(141, 238, 238), text="", font_size=15
    ):
        self.rect = pg.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.text = text
        self.font_size = font_size

    def draw(self, surface):
        pg.draw.rect(surface, self.bg_color, self.rect)
        font = pg.font.Font(font_name, self.font_size)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
