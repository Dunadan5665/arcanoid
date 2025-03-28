from pathlib import Path

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BLUE_DARK = (0, 0, 112)

GREY = (156, 157, 157)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 112, 255)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)

BLOCK_COLORS = (GREY, RED, YELLOW, BLUE, MAGENTA, GREEN)

# цвета дропов
LIME = (150, 255, 50)
AQUAMARINE = (50, 255, 200)
NEON_PINK = (255, 0, 100)
BRIGHT_CORAL = (255, 100, 100)

BLOCK_BORDER_COLOR = WHITE
BG_COLOR = BLUE_DARK
BALL_COLOR = WHITE
RACKET_COLOR = WHITE
MENU_COLOR = WHITE

IS_DEBUG = True
FPS = 60


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
SOUNDS_DIR = ASSETS_DIR / 'sounds'
FONTS_DIR = ASSETS_DIR / 'fonts'
SCORE_FONT = FONTS_DIR / 'PressStart2P-Regular.ttf'
MENU_FONT = FONTS_DIR / 'PressStart2P-Regular.ttf'

BLOCKS_IN_ROW = 6
BLOCK_ROW = 13
