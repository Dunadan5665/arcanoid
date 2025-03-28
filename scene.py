import pygame
from abc import ABC, abstractmethod
import config
from racket import RacketManual
from ball import Ball
from score import Score
from block import Block
from random import randint


class Scene(ABC):
    '''Игровая сцена'''
    @abstractmethod
    def __init__(self, game):
        self.game = game
        self.keys_pressed = None
        self.all_sprites = pygame.sprite.Group()
        self.tile_width = self.game.window_width // config.BLOCK_ROW
        self.tile_height = self.tile_width // 3
        screen_width, screen_height = self.game.screen.get_size()
        min_side = min(screen_width, screen_height)
        self.font_size = int(min_side * 0.03)

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
        self.game.screen.fill(config.BLUE_DARK)
        if config.IS_DEBUG:
            pygame.draw.line(
                self.game.screen,
                config.GREEN,
                (0, self.game.window_height // 2),
                (self.game.window_width, self.game.window_height // 2)
                )
            pygame.draw.line(
                self.game.screen,
                config.WHITE,
                (self.game.window_width // 2, 0),
                (self.game.window_width // 2, self.game.window_height)
                )
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()


class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.all_rackets = pygame.sprite.Group()
        racket_center = (
            int(self.game.window_width // 2),
            int(self.game.window_height * 0.9)
            )
        # ракетка
        self.racket = RacketManual(
            racket_center,
            pygame.K_d,
            pygame.K_a,
            self
            )

        # мяч TODO: спавнить мяч на верхней части ракетки
        self.ball = Ball(self, False, config.BALL_COLOR)

        # табло - набранные очки
        self.score = Score(
            self.game.window_width * 0.5,
            (self.game.window_height * 0.95),
            self,
            'очки',
            lambda: self.ball.score
            )

        # табло - жизни
        self.hp = Score(
            self.game.window_width * 0.9,
            (self.game.window_height * 0.95),
            self,
            'жзни',
            lambda: self.ball.hp
            )
        self.hp.value = self.ball.hp

        self.all_blocks = pygame.sprite.Group()
        self.make_blocks()

        self.all_drops = pygame.sprite.Group()

    def loose(self):
        self.game.scene = MenuScene(self.game, 'Game Over')

    def win(self):
        self.game.scene = MenuScene(self.game, 'WIN')

    def make_blocks(self):
        '''Создаёт блоки'''
        y = self.tile_height
        for i in range(config.BLOCKS_IN_ROW):
            x = 0
            for j in range(config.BLOCK_ROW):
                be_drop = randint(0, 101)
                if be_drop >= 75 and be_drop <= 100:
                    Block(
                        self,
                        (x, y),
                        config.BLOCK_COLORS[i % len(config.BLOCK_COLORS)],
                        True
                    )
                else:
                    Block(
                        self,
                        (x, y),
                        config.BLOCK_COLORS[i % len(config.BLOCK_COLORS)],
                        False
                        )
                x += self.tile_width
            y += self.tile_height

    def create_secondary_ball(self):
        Ball(self, True, config.YELLOW)


class MenuScene(Scene):
    def __init__(self, game, title: str):
        super().__init__(game)
        self.title = title
        self.options = [
            'ENTER - новая игра',
            'ESC - выход'
        ]
        self.make_menu()

    def handle_events(self):
        super().handle_events()
        if self.keys_pressed[pygame.K_RETURN]:
            self.game.scene = GameplayScene(self.game)

    def render(self):
        self.game.screen.fill(config.BLACK)
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()

    def make_menu(self):
        '''Рисует всё меню'''
        total_height = (len(self.options) + 1) * self.font_size * 2
        start_y = (self.game.window_height - total_height) // 2

        self.make_text_sprite(
            (self.game.window_width // 2, start_y),
            self.title,
            self.font_size * 2
        )

        start_y += self.font_size * 3

        for option in self.options:
            self.make_text_sprite(
                (self.game.window_width // 2, start_y),
                option,
                self.font_size
            )
            start_y += self.font_size * 2

    def make_text_sprite(self, coords: tuple, text: str, fdont_size: int):
        '''Рисует одну строку текста'''
        font = pygame.font.Font(config.MENU_FONT, fdont_size)
        sprite = pygame.sprite.Sprite()
        sprite.image = font.render(text, True, config.MENU_COLOR)
        sprite.rect = sprite.image.get_rect(center=coords)
        self.all_sprites.add(sprite)
