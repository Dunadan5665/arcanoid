import config
import pygame


class Score(pygame.sprite.Sprite):
    '''Табло для показа счёта одного из игроков'''
    def __init__(self, center_x: int, center_y: int, scene, title: str, func):
        super().__init__()
        self.scene = scene
        self.center_x = center_x
        self.center_y = center_y
        self.func = func
        self.title = title
        self.color = config.WHITE
        self.size = scene.font_size
        self.font = pygame.font.Font(
            config.SCORE_FONT,
            self.size
            )
        self.image = None
        self.rect = None
        self.scene.all_sprites.add(self)

    def update(self):
        text = f'{self.title}: {self.func()}'
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y
