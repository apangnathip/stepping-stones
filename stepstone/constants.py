import pygame
pygame.font.init()

SCREEN_SIZE = (1280, 800)
FPS = 60

MENU_HEIGHT = 0
MENU_SIZE = (SCREEN_SIZE[0], MENU_HEIGHT)
CTRLBAR_SIZE = 80

MARGIN = 30

BACKGROUND_COLOUR = (51, 51, 51)
HUD_COLOUR = (60, 60, 60)
HUD_COLOUR_SEC = (56, 56, 56)
CTRLBAR_COLOUR = (65, 65, 65)
BUTTON_COLOUR = (80, 80, 80)
BUTTON_ACT_COLOUR = (252, 252, 252)

BOARD_COLOUR_ONE = (56, 27, 11)
BOARD_COLOUR_TWO = (233, 209, 177)
ONES_STONE_COLOUR = (114, 43, 10)
STONE_COLOUR = (185, 178, 171)

HUD_FONT_COLOUR = (252, 252, 252)
HUD_ACT_FONT_COLOUR = (0, 0, 0)
HUD_FONT = pygame.font.SysFont("Consolas", 24, True)