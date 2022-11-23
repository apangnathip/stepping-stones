import sys, pygame
from stepstone.constants import SCREEN_SIZE
from stepstone.board import Board

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

def board_mouse_pos(act_pos):
    x, y = act_pos
    col = x // Board.cell_size
    row = y // Board.cell_size
    return row, col

def main():
    board = Board()
    board.place_stone((1, 2), 1)
    board.place_stone((3, 4), 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = pygame.mouse.get_pressed()
                act_pos = pygame.mouse.get_pos()
                if button_pressed[0]:
                    board_pos = board_mouse_pos(act_pos)
                    board.place_stone(board_pos)

        board.draw(screen)
        pygame.display.flip()

main()