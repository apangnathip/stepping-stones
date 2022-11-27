import pygame
from gui.menu import *
from stepstone.constants import SCREEN_SIZE, MARGIN, HUD_COLOUR, CTRLBAR_SIZE
from stepstone.board import Board

# play_menu = Menu((Button("Reset"), Button("Undo"), Button("Redo"), Button("Search")))

class Hud():
    def __init__(self, menus=[]):
        self.width = SCREEN_SIZE[0] - (Board.rendered_size + MARGIN * 2) - MARGIN
        self.height = SCREEN_SIZE[1] - MARGIN * 2
        self.pos = Board.rendered_size + MARGIN * 2
        self.menus = menus

    def draw(self, screen):
        pygame.draw.rect(screen, HUD_COLOUR, (self.pos, MARGIN, self.width, self.height))
        for menu in self.menus:
            menu.draw(screen)

hud = Hud()
hud.menus.append(Menu(hud, CTRLBAR_SIZE, (Button("Reset"), Button("Undo"), Button("Redo"), Button("Search"))))