import sys, pygame, ctypes
from menu import Menu
from stepstone.constants import SCREEN_SIZE
from stepstone.board import Board

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Stepping Stones")

def board_mouse_pos(act_pos):
    x, y = act_pos
    col = x // Board.cell_size
    row = y // Board.cell_size
    return row, col

def main():
    menu = Menu()
    board = Board()
    board.place_stone((1, 2), 1)
    board.place_stone((3, 4), 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            mouse_pos = pygame.mouse.get_pos()

            for button in menu.buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.hovered = True
                else: button.hovered = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()

                if menu.rect.collidepoint(mouse_pos):
                    if menu.buttons[0].hovered:
                        board = Board() 
                        board.place_stone((1, 2), 1)
                        board.place_stone((3, 4), 1)        
                    if menu.buttons[1].hovered:
                        board.undo()
                    if menu.buttons[2].hovered:
                        board.search()
                else:
                    if mouse_pressed[0]:
                        board_pos = board_mouse_pos(mouse_pos)
                        board.place_stone(board_pos)

        board.draw(screen)
        menu.draw(screen)
        pygame.display.update()

main()