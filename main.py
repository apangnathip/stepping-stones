import pygame
import sys
import ctypes
import threading

from gui.hud import Hud, Button, Slider
from stepstone.board import Board
from stepstone.constants import FPS, SCREEN_SIZE, BACKGROUND_COLOUR, MARGIN, ONES_STONE_COLOUR

pygame.init()
ctypes.windll.user32.SetProcessDPIAware() # Disable scaling on Windows OS
pygame.display.set_caption("Stepping Stones")

icon = pygame.Surface((500, 500))
icon.set_colorkey((0, 0, 0))
pygame.draw.circle(icon, ONES_STONE_COLOUR, (300, 280), 200)
pygame.display.set_icon(icon)

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
    movesets_gen = None
    ctrl_buttons = [
        Button(hud, "set", "top", 3), 
        Button(hud, "reset", "bottom", 0), 
        Button(hud, "undo", "bottom", 1), 
        Button(hud, "redo", "bottom", 2), 
        Button(hud, "solve", "bottom", 3),
        Slider(hud, "size", "top")
    ]

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                board.solving = False
                sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            
            for button in ctrl_buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.hover = True
                else: button.hover = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                for button in ctrl_buttons:
                    if click[0] and button.activated and button.hover:
                        match button.label.lower():
                            case "set":
                                if board.num == 1 and len(board.saved_states) > 1: 
                                    button.activated = False
                                    board.num = 2
                                    board.solving = "quiet"
                                    threading.Thread(target=board.solve).start()
                            case "reset":
                                board.solving = False
                                board = Board(board.size)
                                ctrl_buttons[0].activated = True
                            case "undo":
                                board.solving = False
                                board.traverse("undo")
                                if board.num == 1: ctrl_buttons[0].activated = True
                            case "redo":
                                board.solving = False
                                board.traverse("redo")
                                if board.num > 1: ctrl_buttons[0].activated = False
                            case "solve":
                                if board.num > 1: 
                                    ctrl_buttons[0].activated = False
                                    board.solving = "loud"
                                    threading.Thread(target=board.solve, args=("True",)).start()
                            case "size":
                                button.toggle = True

                if board.rect.collidepoint(mouse_pos):
                    if click[0]:
                        board_pos = board_mouse_pos(mouse_pos, board)
                        board.place_stone(board_pos)
              
            slider_button = ctrl_buttons[5]
            if slider_button.toggle:
                if size := slider_button.change_notch(mouse_pos[0], board.size):
                    board.solving = False
                    ctrl_buttons[0].activated = True
                    board = Board(size)
                if not pygame.mouse.get_pressed()[0]: slider_button.toggle = False

        if board.solved_movesets: 
            board.playing = True
            movesets_gen = board.play_frame(board.solved_movesets)
            board.solved_movesets = None
        if movesets_gen and board.playing: 
            try:
                board.place_stone(next(movesets_gen), check_neighbours=False)
            except StopIteration:
                pass

        screen.fill(BACKGROUND_COLOUR)
        board.draw_stone(screen)
        hud.draw(screen, board)

        for button in ctrl_buttons:
            button.draw(screen)
        pygame.display.update()


main()
