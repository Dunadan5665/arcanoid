import pygame
from drop import Drop
import config
from random import randint


class Block(pygame.sprite.Sprite):
    def __init__(self, scene, coords: tuple, color: tuple, is_drop: bool):
        super().__init__()
        self.scene = scene
        self.coords = coords
        self.color = color
        self.is_drop = is_drop
        self.image = pygame.Surface(
            (
                self.scene.tile_width,
                self.scene.tile_height
                )
                )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords
        self.scene.all_sprites.add(self)
        self.scene.all_blocks.add(self)
        self.bonus = 1

        pygame.draw.rect(
            self.image,
            config.BLOCK_BORDER_COLOR,
            self.image.get_rect(),
            1
        )

    def destroy(self):
        self.scene.ball.score += self.bonus
        self.kill()
        if self.is_drop:
            probability_color_drop = randint(0, 101)
            if probability_color_drop >= 0 and probability_color_drop <= 50:
                Drop(self.scene, self.rect.center, config.BRIGHT_CORAL)

            elif probability_color_drop >= 51 and \
                    probability_color_drop <= 75:
                Drop(self.scene, self.rect.center, config.LIME)

            elif probability_color_drop >= 76 and \
                    probability_color_drop <= 100:
                Drop(self.scene, self.rect.center, config.NEON_PINK)

        if not self.scene.all_blocks:
            self.scene.win()
