from pygame import gfxdraw
from .constants import *


class Board:
    def __init__(self, size=12):
        self.size = size
        self.cell_size = (SCREEN_SIZE[1] - MENU_HEIGHT - MARGIN * 2) // size
        self.rendered_size = size * self.cell_size

        self.board = [[0] * self.size for _ in range(self.size)]
        self.sum_board = [[0] * self.size for _ in range(self.size)]
        self.stone_size = self.cell_size // 2
        self.num = 1
        self.saved_states = [[[0] * self.size for _ in range(self.size)]]
        self.rect = pygame.Rect(MARGIN, MARGIN, self.rendered_size, MENU_HEIGHT + self.rendered_size)

        self.highest = None
        self.solving = False
        self.solved_movesets = None

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
        self.board = self.saved_states[curr_state + operation]

    def neighbour_sum(self, override_board=None, prev_sums=None, c_pos=None):
        if override_board:
            board = override_board
        else:
            board = self.board

        if prev_sums is None:
            sums = {}
            for row in range(self.size):
                for col in range(self.size):
                    if board[row][col]: continue
                    sum = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0 or row+i < 0 or col+j < 0: continue
                            try:
                                sum += board[row + i][col + j]
                            except IndexError:
                                continue
                    if sum not in sums:
                        sums[sum] = set()
                    sums[sum].add((row, col))
            return sums

        row = c_pos[0]
        col = c_pos[1]
        board_num = board[row][col]
        sums = {}
        iter_sums = {}

        for key, value in prev_sums.items():
            sums[key] = value.copy()
            iter_sums[key] = value.copy()
        sums[board_num].remove(c_pos)
        iter_sums[board_num].remove(c_pos)
        iter_sums = iter_sums.items()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                for key, value in iter_sums:
                    for pos in value:
                        if pos == (row+i, col+j):
                            sums[key].remove(pos)
                            new_sum = key + board_num
                            if new_sum not in sums:
                                sums[new_sum] = set()
                            sums[new_sum].add(pos)                        
                            break
                    else: continue
                    break            
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

    def place_stone(self, pos, num=None):
        if not self.board[pos[0]][pos[1]]:
            sums = self.neighbour_sum()
            if self.num == 1:
                self.board[pos[0]][pos[1]] = 1
            elif num:
                self.board[pos[0]][pos[1]] = num
            elif self.num in sums and pos in sums[self.num]:
                curr_state = self.saved_states.index(self.board)
                if curr_state != len(self.saved_states) - 1:
                    self.saved_states = [state[:] for state in self.saved_states][:curr_state + 1]
                self.board[pos[0]][pos[1]] = self.num
                self.num += 1
            self.saved_states.append([row[:] for row in self.board])

    def play_frame(self, movesets):
        saved = ()
        for moveset in movesets:
            if moveset != movesets[-1]: 
                saved = ([row[:] for row in self.board], self.num)
            else: saved = ()
            for move in moveset:
                yield move
            if saved: self.board, self.num = saved

    def play_all(self, moveset):
        for move in moveset:
            self.place_stone(move)
  
    def solve(self, get_moves=False):
        best_moves = []
        num = self.num
        num_reached = []

        def auto_place(curr_num, curr_board, curr_sums, moves):
            if curr_num not in curr_sums:
                num_reached.append(1)
                return
            for pos in curr_sums[curr_num]:
                next_board = [row[:] for row in curr_board]
                next_board[pos[0]][pos[1]] = curr_num
                next_moves = moves[:]
                next_moves.append(pos)
                next_sums = self.neighbour_sum(next_board, curr_sums, pos)
                if curr_num + 1 in next_sums and next_sums[curr_num+1]:
                    auto_place(curr_num + 1, next_board, next_sums, next_moves)
                elif curr_num not in num_reached:
                    best_moves.append(next_moves)
                    num_reached.append(curr_num)
        auto_place(num, self.board, self.neighbour_sum(self.board), [])

        if get_moves: 
            self.solved_movesets = sorted(best_moves, key=len)
        else: 
            self.highest = max(num_reached)
        self.solving = False
    
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
    
