import pygame
import config

'''
шанс дропа в целом
Лаймовый - два мяча
Аквамарин - увеличение ширины ракетки
Розовый - + 1 жизнь
Кораловый - +5 очков
'''


class Drop(pygame.sprite.Sprite):
    def __init__(self, scene, center_coords: tuple, color: tuple):
        super().__init__()
        self.scene = scene
        self.color = color
        self.image = pygame.Surface(
            (
                self.scene.tile_height,
                self.scene.tile_height
                )
                )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = center_coords
        self.scene.all_sprites.add(self)
        self.scene.all_drops.add(self)
        self.speed = 5
        self.sound = {
            'power_hp': pygame.mixer.Sound(config.SOUNDS_DIR / 'power_hp.wav'),
            'new_ball': pygame.mixer.Sound(config.SOUNDS_DIR / 'new_ball.wav'),
            'points': pygame.mixer.Sound(config.SOUNDS_DIR / 'points.wav')
        }

    def move(self):
        self.rect.y += self.speed

    def collide_bottom(self):
        if self.rect.bottom > self.scene.game.window_height:
            self.kill()

    def collide_rackets(self):
        rackets_hit = pygame.sprite.spritecollide(
            self,
            self.scene.all_rackets,
            False
            )
        if not rackets_hit:
            return
        self.function_of_drop()
        self.kill()

    def function_of_drop(self):
        if self.color == config.BRIGHT_CORAL:
            self.scene.ball.score += 5
            self.sound['points'].play()

        elif self.color == config.LIME:
            self.scene.create_secondary_ball()
            self.sound['new_ball'].play()

        elif self.color == config.NEON_PINK:
            if self.scene.ball.hp < 3:
                self.scene.ball.hp += 1
                self.sound['power_hp'].play()

    def update(self):
        self.move()
        self.collide_bottom()
        self.collide_rackets()
