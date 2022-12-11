from pygame import gfxdraw
from .constants import *
from copy import deepcopy


class Board:
    def __init__(self, size=BOARD_SIZES[2]):
        self.size = size
        self.cell_size = (SCREEN_SIZE[1] - MENU_HEIGHT - MARGIN * 2) // size
        self.rendered_size = size * self.cell_size

        self.rect = pygame.Rect(MARGIN, MARGIN, self.rendered_size, MENU_HEIGHT + self.rendered_size)
        self.board = [[0] * self.size for _ in range(self.size)]
        self.sum_board = [[0] * self.size for _ in range(self.size)]
        self.stone_margin = self.cell_size // 12
        self.stone_size = self.cell_size // 2 - self.stone_margin
        self.stone_font = pygame.font.SysFont("Consolas", self.cell_size // 2)
        self.num = 1

        self.playing = False
        self.branch_num = 0
        self.saved_states = [[[0] * self.size for _ in range(self.size)]]
        self.num_reached = []
        self.highest_num = None
        self.solving = False # 3 Modes: loud, shows solving; quiet, solve in background; False
        self.solved_movesets = None

    # Undo/Redo functions
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
            if self.num > 1: self.num += 1
            operation = 1
        self.board = deepcopy(self.saved_states)[curr_state+operation]

    # Find the sums of each cells by their neighbours
    def neighbour_sum(self, override_board=None, prev_sums=None, c_pos=None):
        if override_board:
            board = override_board
        else: board = self.board

        if prev_sums is None: # Only triggers on initial one's stone configuration
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

    # DEBUGGING PURPOSES; Prints the sum by neighbours of the current board
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

    # Places stone if their placement is legal
    def place_stone(self, pos, num=None, check_neighbours=True):
        if not self.board[pos[0]][pos[1]]:
            curr_state = self.saved_states.index(self.board)
            if check_neighbours: sums = self.neighbour_sum()
            if self.num == 1:
                self.board[pos[0]][pos[1]] = 1
            elif num:
                self.board[pos[0]][pos[1]] = num
            elif not check_neighbours or self.num in sums and pos in sums[self.num]:
                self.board[pos[0]][pos[1]] = self.num
                self.num += 1
            if curr_state != len(self.saved_states) - 1:
                self.saved_states = [state[:] for state in self.saved_states][:curr_state+1]
                self.saved_states = self.saved_states[:curr_state+1]
            self.saved_states.append([row[:] for row in self.board])

    # Solve the board based on current board configuration
    def solve(self, get_moves=False):
        best_moves = []
        num = self.num
        state = self.solving
        self.num_reached = []

        def auto_place(curr_num, curr_board, curr_sums, moves):
            if self.solving != state: return
            if curr_num not in curr_sums:
                self.num_reached.append(1)
                return
            for pos in curr_sums[curr_num]:
                next_board = [row[:] for row in curr_board]
                next_board[pos[0]][pos[1]] = curr_num
                next_moves = moves[:]
                next_moves.append(pos)
                next_sums = self.neighbour_sum(next_board, curr_sums, pos)
                if curr_num + 1 in next_sums and next_sums[curr_num+1]:
                    auto_place(curr_num + 1, next_board, next_sums, next_moves)
                    continue
                if not self.num_reached or curr_num not in self.num_reached and curr_num > self.num_reached[-1]:
                    best_moves.append(next_moves)
                    self.num_reached.append(curr_num)
                self.branch_num += 1
        auto_place(num, self.board, self.neighbour_sum(self.board), [])

        if self.solving != state: return
        if get_moves: 
            self.solved_movesets = sorted(best_moves, key=len)
        if not get_moves or num == 2: 
            self.highest_num = self.num_reached[-1]

        self.solving = False
        self.branch_num = 0
    
    def draw_board(self, screen):
        screen.fill(BOARD_COLOUR_ONE, (MARGIN, MARGIN, self.rendered_size, self.rendered_size))
        for row in range(self.size):
            for col in range(row % 2, self.size, 2):
                pygame.draw.rect(screen, BOARD_COLOUR_TWO, (
                    col * self.cell_size + MARGIN, row * self.cell_size + MENU_SIZE[1] + MARGIN, self.cell_size,
                    self.cell_size))

    def draw_stone(self, screen):
        self.draw_board(screen)
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    centre_pos = (col * self.cell_size + self.stone_size + self.stone_margin + MARGIN,
                    row * self.cell_size + self.stone_size + self.stone_margin + MENU_SIZE[1] + MARGIN)

                    if self.board[row][col] == 1:
                        gfxdraw.aacircle(screen, centre_pos[0], centre_pos[1], self.stone_size, ONES_STONE_COLOUR)
                        gfxdraw.filled_circle(screen, centre_pos[0], centre_pos[1], self.stone_size, ONES_STONE_COLOUR)
                        continue
                    
                    gfxdraw.aacircle(screen, centre_pos[0], centre_pos[1], self.stone_size, STONE_COLOUR)
                    gfxdraw.filled_circle(screen, centre_pos[0], centre_pos[1], self.stone_size, STONE_COLOUR)

                    number = self.stone_font.render(f"{self.board[row][col]}", True, (0, 0, 0))
                    screen.blit(number, (centre_pos[0] - number.get_width()/2, centre_pos[1] - number.get_height()/2.5))
    
    # Return each board configuration from a list of movesets every program loop
    def play_frame(self, movesets):
        saved = ()
        for moveset in movesets:
            if moveset != movesets[-1]: 
                saved = ([row[:] for row in self.board], self.num)
            else: saved = ()
            for move in moveset:
                yield move
            if saved: self.board, self.num = saved

