import ctypes
import pygame
import sys

from gui.hud import Hud, hud
from gui.menu import Menu, Button
from stepstone.board import Board
from stepstone.constants import SCREEN_SIZE, BACKGROUND_COLOUR, MARGIN

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Stepping Stones")


def board_mouse_pos(act_pos):
    x, y = act_pos
    row = (y - MARGIN) // Board.cell_size
    col = (x - MARGIN) // Board.cell_size
    return row, col


def main():
    board = Board(6)
    board.place_stone((1, 2), 1)
    board.place_stone((3, 4), 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            mouse_pos = pygame.mouse.get_pos()

            # for button in menu.buttons:
            #     if button.rect.collidepoint(mouse_pos):
            #         button.hovered = True
            #     else:
            #         button.hovered = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()

                if board.rect.collidepoint(mouse_pos):
                    if mouse_pressed[0]:
                        board_pos = board_mouse_pos(mouse_pos)
                        board.place_stone(board_pos)
                        
            #     if menu.rect.collidepoint(mouse_pos):
            #         if menu.buttons[0].hovered:
            #             board = Board()
            #             board.place_stone((1, 2), 1)
            #             board.place_stone((3, 4), 1)
            #         if menu.buttons[1].hovered:
            #             board.undo()
            #         if menu.buttons[2].hovered:
            #             board.search()

        screen.fill(BACKGROUND_COLOUR)
        board.draw(screen)
        hud.draw(screen)
        pygame.display.update()


main()
