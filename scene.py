import pygame
import math
from abc import ABC, abstractmethod
import config
from racket import RacketManual, Racketauto, Racket
from ball import Ball
from score import Score
from block import Block, BonusBlock


class Scene(ABC):
    '''Игровая сцена'''
    @abstractmethod
    def __init__(self, game):
        self.game = game
        self.keys_pressed = None
        self.all_sprites = pygame.sprite.Group()
        self.tile_size = math.gcd(self.game.window_width, self.game.window_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.is_running = False

        self.keys_pressed = pygame.key.get_pressed()

    def update(self):
        self.all_sprites.update()

    def render(self):
        pass

class GameplayScene(Scene):
    def __init__(self, game, mode: str):
        super().__init__(game)
        self.all_rackets = pygame.sprite.Group()
        racket_center = (int(self.game.window_width // 2), int(self.game.window_height * 0.9))
        # ракетка
        if mode == 'human':    
            self.racket = RacketManual(racket_center, pygame.K_d, pygame.K_a, self)
        else:
            self.racket = Racketauto(racket_center, self, 20)
        
        # мяч TODO: спавнить мяч на верхней части ракетки
        self.ball = Ball(self)

        # табло - набранные очки
        self.score = Score(
            self.game.window_width * 0.5,
            (self.game.window_height * 0.95),
            self,
            lambda: self.ball.score
            )

        # табло - жизни
        self.hp = Score(
            self.game.window_width * 0.9,
            (self.game.window_height * 0.95),
            self,
            lambda: self.ball.hp
            )
        self.hp.value = self.ball.hp

        self.all_blocks = pygame.sprite.Group()
        self.make_blocks()

    def make_blocks(self):
        '''Создаёт блоки'''
        y = self.tile_size
        for i in range(config.BLOCKS_IN_ROW):
            x = 0
            for j in range(self.game.window_width // self.tile_size):
                if i % 2:
                    Block(self, (x, y))
                else:
                    BonusBlock(self, (x, y))
                x += self.tile_size
            y += self.tile_size

    def render(self):
        self.game.screen.fill(config.BLACK)
        if config.IS_DEBUG:
            pygame.draw.line(self.game.screen, config.GREEN, (0, self.game.window_height // 2), (self.game.window_width, self.game.window_height // 2))
            pygame.draw.line(self.game.screen, config.WHITE, (self.game.window_width // 2, 0), (self.game.window_width // 2, self.game.window_height))
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()
    
    def loose(self):
        self.game.scene = MenuScene(self.game, 'Game Over')


class MenuScene(Scene):
    def __init__(self, game, heading: str):
        super().__init__(game)
        MenuLines(
            self,
            heading,
            '1 - человек',
            '2 - компьютер',
            'ESC - выход'
        )

    def handle_events(self):
        super().handle_events()
        if self.keys_pressed[pygame.K_2]:
            self.game.scene = GameplayScene(self.game, 'human_vs_pc')
        elif self.keys_pressed[pygame.K_1]:
            self.game.scene = GameplayScene(self.game, 'human')

    def render(self):
        self.game.screen.fill(config.BLACK)
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()


class TextLine(pygame.sprite.Sprite):
    def __init__(self, scene, text_line: str, coords: tuple):
        super().__init__()
        self.font = pygame.font.Font(None, 100)
        self.image = self.font.render(text_line, True, config.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        scene.all_sprites.add(self)


class MenuLines:
    def __init__(self, scene, heading, *lines):
        x = scene.game.window_width // 2
        y = 100
        TextLine(scene, heading, (x, y))
        for line in lines:
            y += 100
            TextLine(scene, line, (x, y))
