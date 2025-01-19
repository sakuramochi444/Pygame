import pygame as pg
import data as d

class Stage0:
    def __init__(self, chip_size):
        self.chip_size = chip_size
        self.font = pg.font.Font(None, 74)  # 大きなフォント
        self.sub_font = pg.font.Font(None, 36)  # 小さなフォント

    def draw(self, screen):
        screen.fill(pg.Color('WHITE'))  # 背景を白に設定
        title_surface = self.font.render("白黒パズル", True, pg.Color('BLACK'))
        subtitle_surface = self.sub_font.render("SPACEキーを押してスタート！", True, pg.Color('BLACK'))

        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        subtitle_rect = subtitle_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))

        screen.blit(title_surface, title_rect)
        screen.blit(subtitle_surface, subtitle_rect)