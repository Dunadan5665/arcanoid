from abc import ABC, abstractmethod
import config
import pygame


class Racket(ABC, pygame.sprite.Sprite):
    width = 10
    height = 65
    speed = 10

    @abstractmethod
    def __init__(self, center: tuple, scene):
        super().__init__()
        self.scene = scene
        self.center = center
        self.color = config.RACKET_COLOR
        self.speed = 10  # Racket.speed
        self.image = pygame.Surface(
            (
                self.scene.tile_width,
                int(self.scene.tile_height * 0.3)
                )
                )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.goto_start()
        self.direction = 0
        self.scene.all_sprites.add(self)
        self.scene.all_rackets.add(self)

    def goto_start(self):
        self.rect.center = self.center

    def move(self):
        '''Двигает ракетку'''
        pass

    def collide_borders(self):
        if self.rect.right > self.scene.game.window_width:
            self.rect.right = self.scene.game.window_width
        elif self.rect.left < 0:
            self.rect.left = 0

    def update(self):
        self.move()
        self.collide_borders()


class RacketManual(Racket):
    def __init__(self, center, key_right, key_left, scene):
        super().__init__(center, scene)
        self.key_right = key_right
        self.key_left = key_left

    def move(self):
        if not self.scene.keys_pressed:
            self.direction = 0
            return
        if self.scene.keys_pressed[self.key_right]:
            self.rect.x += self.speed
            self.direction = 1
        elif self.scene.keys_pressed[self.key_left]:
            self.rect.x -= self.speed
            self.direction = -1
