import pygame
pygame.font.init()

MENU_HEIGHT = 25
SCREEN_SIZE = (1000, 1000 + MENU_HEIGHT)
MENU_SIZE = (SCREEN_SIZE[0], MENU_HEIGHT)

MENU_COLOUR = (255, 255, 255)
COLOUR_ONE = (56, 27, 11)
COLOUR_TWO = (233, 209, 177)
STONE_COLOUR = (185, 178, 171)

MENU_FONT = pygame.font.SysFont("Segoe UI", 18)
STONE_FONT = pygame.font.SysFont("Segoe UI", 36)