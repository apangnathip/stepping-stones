import pygame
import sys
import ctypes
import threading

from gui.hud import Hud, Button
from stepstone.board import Board
from stepstone.constants import FPS, SCREEN_SIZE, BACKGROUND_COLOUR, MARGIN

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
pygame.display.set_caption("Stepping Stones")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
    

def board_mouse_pos(act_pos, board):
    x, y = act_pos
    row = (y - MARGIN) // board.cell_size
    col = (x - MARGIN) // board.cell_size
    return row, col


def main():
    board = Board()
    hud = Hud(board)
    ctrl_buttons = [Button(hud, "Set", "top", 3), Button(hud, "reset", "bottom", 0), Button(hud, "undo", "bottom", 1), Button(hud, "redo", "bottom", 2), Button(hud, "solve", "bottom", 3)]
    movesets_gen = None

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            
            for button in ctrl_buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.hover = True
                else: button.hover = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()

                for button in ctrl_buttons:
                    if mouse_pressed[0] and button.activated and button.hover:
                        match button.label.lower():
                            case "set":
                                if board.num == 1 and len(board.saved_states) > 1: 
                                    button.activated = False
                                    board.num = 2
                                    board.solving = "quiet"
                                    threading.Thread(target=board.solve).start()
                            case "reset":
                                board.solving = False
                                board = Board()
                                ctrl_buttons[0].activated = True
                                break
                            case "undo":
                                board.traverse("undo")
                                if board.num == 1: ctrl_buttons[0].activated = True
                                break
                            case "redo":
                                board.traverse("redo")
                                if board.num > 1: ctrl_buttons[0].activated = False
                                break
                            case "solve":
                                if board.num > 1: 
                                    board.solving = "loud"
                                    ctrl_buttons[0].activated = False
                                    threading.Thread(target=board.solve, args=("True",)).start()
                                break

                if board.rect.collidepoint(mouse_pos):
                    if mouse_pressed[0]:
                        board_pos = board_mouse_pos(mouse_pos, board)
                        board.place_stone(board_pos)

        if board.solved_movesets: 
            movesets_gen = board.play_frame(board.solved_movesets)
            board.solved_movesets = None
        if movesets_gen: 
            try:
                board.place_stone(next(movesets_gen), check_neighbours=False)
            except StopIteration:
                pass

        screen.fill(BACKGROUND_COLOUR)
        board.draw(screen)
        hud.draw(screen, board)

        for button in ctrl_buttons:
            button.draw(screen)
        pygame.display.update()


main()
