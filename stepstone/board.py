from copy import deepcopy
from pygame import gfxdraw
from .constants import *


class Board:
    size = 6
    cell_size = (SCREEN_SIZE[1] - MENU_HEIGHT - MARGIN * 2) // size
    rendered_size = size * cell_size

    def __init__(self, size):
        self.size = size
        self.cell_size = (SCREEN_SIZE[1] - MENU_HEIGHT - MARGIN * 2) // size
        self.rendered_size = size * self.cell_size
        self.board = [[0] * Board.size for _ in range(Board.size)]
        self.sum_board = [[0] * Board.size for _ in range(Board.size)]
        self.stone_size = Board.cell_size // 2
        self.num = 2
        self.highest = []
        self.saved_states = []
        self.rect = pygame.Rect(MARGIN, MARGIN, Board.rendered_size, MENU_HEIGHT + Board.rendered_size)

    def undo(self):
        if self.num != 2:
            self.num -= 1
            self.board = self.saved_states[-1]
            self.saved_states.pop()

    def neighbour_sum(self, ov_board=None):
        if ov_board:
            board = ov_board
        else:
            board = self.board

        sums = {}
        for row in range(Board.size):
            for col in range(Board.size):
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

        for row in range(Board.size):
            for col in range(Board.size):
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

    def place_stone(self, pos, num=None):
        self.saved_states.append(deepcopy(self.board))
        sums = self.neighbour_sum()
        if not self.board[pos[0]][pos[1]]:
            if self.num == 1:
                self.board[pos[0]][pos[1]] = 1
            if num:
                self.board[pos[0]][pos[1]] = num
            elif self.num in sums and pos in sums[self.num]:
                self.board[pos[0]][pos[1]] = self.num
                self.num += 1
        # self.draw_sum_board(self.neighbour_sum())

    def play(self, move_set):
        for move in move_set:
            self.place_stone(move)
  
    def search(self):
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
        screen.fill(COLOUR_ONE, (MARGIN, MARGIN, Board.rendered_size, MENU_HEIGHT + Board.rendered_size))
        for row in range(Board.size):
            for col in range(row % 2, Board.size, 2):
                pygame.draw.rect(screen, COLOUR_TWO, (
                    col * Board.cell_size + MARGIN, row * Board.cell_size + MENU_SIZE[1] + MARGIN, Board.cell_size,
                    Board.cell_size))

    def draw(self, screen):
        self.draw_board(screen)
        for row in range(Board.size):
            for col in range(Board.size):
                if self.board[row][col] != 0:
                    centre_pos = (row * Board.cell_size + self.stone_size + MENU_SIZE[1] + MARGIN,
                                  col * Board.cell_size + self.stone_size + MARGIN)

                    gfxdraw.aacircle(screen, centre_pos[1], centre_pos[0], self.stone_size - 10, STONE_COLOUR)
                    gfxdraw.filled_circle(screen, centre_pos[1], centre_pos[0], self.stone_size - 10, STONE_COLOUR)

                    number = STONE_FONT.render(f"{self.board[row][col]}", True, (0, 0, 0))
                    rect = number.get_rect()
                    rect.centery, rect.centerx = centre_pos
                    screen.blit(number, rect)
