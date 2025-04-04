import config
import math
import pygame


class Ball(pygame.sprite.Sprite):
    width = 20
    height = 20
    speed = 10

    def __init__(self, scene, is_secondary: bool, color):
        super().__init__()
        self.scene = scene
        self.is_secondary = is_secondary
        self.velocity_x = 0
        self.velocity_y = 0
        self.angle = 135  # в градусах
        self.color = color
        self.speed = 10  # px / Frame
        self.hp = 3
        self.score = 0

        width = self.scene.tile_height // 2
        height = self.scene.tile_height // 2

        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.goto_start()
        self.sound = {
            'collide': pygame.mixer.Sound(config.SOUNDS_DIR / 'collide.wav'),
            'lose': pygame.mixer.Sound(config.SOUNDS_DIR / 'lose.wav'),
            'win': pygame.mixer.Sound(config.SOUNDS_DIR / 'win.wav')
        }
        self.scene.all_sprites.add(self)

    def goto_start(self):
        self.rect.midbottom = self.scene.racket.rect.midtop
        self.angle = 0

    def move(self):
        self.velocity_x = math.cos(math.radians(self.angle - 90))
        self.velocity_y = math.sin(math.radians(self.angle - 90))
        self.rect.x += self.velocity_x * self.speed
        self.rect.y += self.velocity_y * self.speed

    def collide_borders(self):
        'Столкновения с границами экрана'
        if self.rect.left < 0 or \
                self.rect.right > self.scene.game.window_width:
            self.angle = (360 - self.angle) % 360
            self.sound['collide'].play()
        elif self.rect.top < 0:
            self.angle = (180 - self.angle) % 360
            self.sound['collide'].play()

    def collide_rackets(self):
        'Столкновения с ракетками'
        rackets_hit = pygame.sprite.spritecollide(
            self,
            self.scene.all_rackets,
            False
            )
        if not rackets_hit:
            return

        racket_hit = rackets_hit[0]
        сollision_point = self.rect.centerx - racket_hit.rect.left
        if сollision_point < racket_hit.rect.width / 3:
            self.angle = -30
        elif сollision_point > racket_hit.rect.width / 3 * 2:
            self.angle = 30
        else:
            self.angle = 0

        self.rect.bottom = racket_hit.rect.top - 1
        self.sound['collide'].play()

    def collide_blocks(self):
        'Столкновения с блоками'
        blocks_hit = pygame.sprite.spritecollide(
            self,
            self.scene.all_blocks,
            True
            )
        if blocks_hit:
            for block in blocks_hit:
                self.sound['win'].play()
                block.destroy()
            self.angle = (180 - self.angle) % 360

    def check_lose(self) -> None:
        '''Мяч ушёл вниз'''
        if self.rect.bottom > self.scene.game.window_height:
            if not self.is_secondary:
                self.hp -= 1
                self.scene.hp.value -= 1
                if self.hp > 0:
                    self.scene.racket.goto_start()
                    self.goto_start()
                    self.sound['lose'].play()
                else:
                    self.scene.loose()
                    self.kill()
            else:
                self.kill()

    def render(self):
        pygame.draw.rect(self.scene.game.screen, self.color, self.rect, 0)

    def update(self):
        self.move()
        self.check_lose()
        self.collide_borders()
        self.collide_rackets()
        self.collide_blocks()
