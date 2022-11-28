from copy import deepcopy
from pygame import gfxdraw
from .constants import *


class Board:
    def __init__(self, size=6):
        self.size = size
        self.cell_size = (SCREEN_SIZE[1] - MENU_HEIGHT - MARGIN * 2) // size
        self.rendered_size = size * self.cell_size

        self.board = [[0] * self.size for _ in range(self.size)]
        self.sum_board = [[0] * self.size for _ in range(self.size)]
        self.stone_size = self.cell_size // 2
        self.num = 1
        self.highest = []
        self.saved_states = [[[0] * self.size for _ in range(self.size)]]
        self.rect = pygame.Rect(MARGIN, MARGIN, self.rendered_size, MENU_HEIGHT + self.rendered_size)

    def traverse(self, mode):
        try:
            curr_state = self.saved_states.index(self.board)
        except ValueError:
            return

        if mode == "undo": 
            if curr_state == 0: return
            if self.num != 1: self.num -= 1
            operation = -1 
        if mode == "redo":
            if curr_state == len(self.saved_states) - 1: return
            self.num += 1
            operation = 1

        # if mode == "undo" and curr_state != 0 or mode == "redo" and curr_state != len(self.saved_states) - 1:
        self.board = self.saved_states[curr_state + operation]

    def neighbour_sum(self, ov_board=None):
        if ov_board:
            board = ov_board
        else:
            board = self.board

        sums = {}
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col]: continue
                sum = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if row + i < 0 or col + j < 0: continue
                        try:
                            sum += board[row + i][col + j]
                        except IndexError:
                            continue
                if sum > 1:
                    if sum not in sums:
                        sums[sum] = set()
                    sums[sum].add((row, col))
        return sums

    # DEBUGGING PURPOSES
    def draw_sum_board(self, sums):
        for key, value in sums.items():
            for pos in value:
                if self.board[pos[0]][pos[1]]:
                    self.sum_board[pos[0]][pos[1]] = 0
                    continue
                self.sum_board[pos[0]][pos[1]] = key

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col]:
                    print(f"\033[91m{self.board[row][col]}\033[00m", end=" ")
                elif self.sum_board[row][col] != 0:
                    if self.sum_board[row][col] == self.num:
                        print(f"\033[96m{self.sum_board[row][col]}\033[00m", end=" ")
                    else:
                        print(f"\033[97m{self.sum_board[row][col]}\033[00m", end=" ")
                else:
                    print(0, end=" ")
            print()
        print()

    # ! UNDO AND REDO DOES NOT WORK WHEN A CHANGE IS MADE WHEN IN A SAVED STATE
    def place_stone(self, pos, num=None):
        if not self.board[pos[0]][pos[1]]:
            sums = self.neighbour_sum()
            if self.num == 1:
                self.board[pos[0]][pos[1]] = 1
            if num:
                self.board[pos[0]][pos[1]] = num
            elif self.num in sums and pos in sums[self.num]:
                curr_state = self.saved_states.index(self.board)
                if curr_state != len(self.saved_states) - 1:
                    self.saved_states = deepcopy(self.saved_states)[:curr_state + 1]
                self.board[pos[0]][pos[1]] = self.num
                self.num += 1

            self.saved_states.append(deepcopy(self.board))

    def play(self, move_set):
        for move in move_set:
            self.place_stone(move)
  
    def solve(self):
        best_moves = []
        board = self.board
        num = self.num
        num_reached = [0]

        def recursive_placing(curr_num, curr_board, moves):
            sums = self.neighbour_sum(curr_board)
            if curr_num not in sums:
                if curr_num - 1 > num_reached[0]:
                    num_reached.append(curr_num - 1)
                    num_reached[0] = curr_num - 1
                    best_moves.append(moves)
                return
            for pos in sums[curr_num]:
                next_board = deepcopy(curr_board)
                next_board[pos[0]][pos[1]] = curr_num
                next_moves = moves[:]
                next_moves.append(pos)
                recursive_placing(curr_num + 1, next_board, next_moves)

        recursive_placing(num, board, [])
        self.play(best_moves[-1])
    
    def draw_board(self, screen):
        screen.fill(BOARD_COLOUR_ONE, (MARGIN, MARGIN, self.rendered_size, MENU_HEIGHT + self.rendered_size))
        for row in range(self.size):
            for col in range(row % 2, self.size, 2):
                pygame.draw.rect(screen, BOARD_COLOUR_TWO, (
                    col * self.cell_size + MARGIN, row * self.cell_size + MENU_SIZE[1] + MARGIN, self.cell_size,
                    self.cell_size))

    def draw(self, screen):
        self.draw_board(screen)
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    centre_pos = (row * self.cell_size + self.stone_size + MENU_SIZE[1] + MARGIN,
                                  col * self.cell_size + self.stone_size + MARGIN)

                    if self.board[row][col] == 1:
                        gfxdraw.aacircle(screen, centre_pos[1], centre_pos[0], self.stone_size - 10, ONES_STONE_COLOUR)
                        gfxdraw.filled_circle(screen, centre_pos[1], centre_pos[0], self.stone_size - 10, ONES_STONE_COLOUR)
                    else:
                        gfxdraw.aacircle(screen, centre_pos[1], centre_pos[0], self.stone_size - 10, STONE_COLOUR)
                        gfxdraw.filled_circle(screen, centre_pos[1], centre_pos[0], self.stone_size - 10, STONE_COLOUR)

                        number = STONE_FONT.render(f"{self.board[row][col]}", True, (0, 0, 0))
                        rect = number.get_rect()
                        rect.centery, rect.centerx = centre_pos
                        screen.blit(number, rect)
    
