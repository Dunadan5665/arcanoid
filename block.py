import pygame
import config
import random


class Block(pygame.sprite.Sprite):
    def __init__(self, scene, coords: tuple):
        super().__init__()
        self.scene = scene
        self.color = config.BASE_BLOCK_COLOR
        self.image = pygame.Surface((self.scene.tile_size, self.scene.tile_size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.scene.all_sprites.add(self)
        self.scene.all_blocks.add(self)
        self.bonus = 1

    def destroy(self):
        self.scene.ball.score += self.bonus
        self.kill()


class BonusBlock(Block):
    def __init__(self, scene, coords):
        super().__init__(scene, coords)
        self.color = config.BONUS_BLOCK_COLOR
        self.image = pygame.Surface((self.scene.tile_size, self.scene.tile_size))
        self.image.fill(self.color)
        self.bonus = 10
    
    def destroy(self):
        self.scene.ball.score += self.bonus
        self.kill()
