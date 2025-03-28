import pygame
import config
from scene import MenuScene


class Game:
    '''Игра'''
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        display_info = pygame.display.Info()
        self.window_width = display_info.current_w
        self.window_height = display_info.current_h
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        self.scene = MenuScene(self, 'ARCANOID')
        self.keys_pressed = None
        self.is_running = True
        self.clock = pygame.time.Clock()

    def main_loop(self) -> None:
        '''
        Сбор событий
        Обновление (объектов)
        Рендер (отрисовка)
        '''
        while self.is_running:
            self.scene.handle_events()
            self.scene.update()
            self.scene.render()
            self.clock.tick(config.FPS)
        pygame.quit()

    def handle_events(self) -> None:
        '''Обрабатывает события'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

        self.keys_pressed = pygame.key.get_pressed()

    def update(self) -> None:
        self.scene.all_sprites.update()

    def render(self):
        '''Отрисовывает объекты на экране'''
        self.screen.fill(config.BLUE_DARK)
        if config.IS_DEBUG:
            pygame.draw.line(
                self.screen,
                config.RED,
                (int(self.window_width * 0.1), 0),
                (int(self.window_width * 0.1), self.window_width)
                )
            pygame.draw.line(
                self.screen,
                config.RED,
                (int(self.window_width * 0.9), 0),
                (int(self.window_width * 0.9),
                 self.window_width)
                 )
            pygame.draw.line(
                self.screen,
                config.GREEN,
                (0, self.window_height // 2),
                (self.window_width,
                 self.window_height // 2)
                 )
        pygame.draw.line(
            self.screen,
            config.WHITE,
            (self.window_width // 2, 0),
            (self.window_width // 2, self.window_height)
            )
        self.scene.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.main_loop()
