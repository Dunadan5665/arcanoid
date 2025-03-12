from pathlib import Path

RED = (255, 0, 0)  # RGB
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

BASE_BLOCK_COLOR = WHITE
BONUS_BLOCK_COLOR = RED

IS_DEBUG = True
FPS = 60


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
SOUNDS_DIR = ASSETS_DIR / 'sounds'
FONTS_DIR = ASSETS_DIR / 'fonts'

BLOCKS_IN_ROW = 3