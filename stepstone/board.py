import pygame
from pygame import gfxdraw
from .constants import SCREEN_SIZE, COLOUR_ONE, COLOUR_TWO, STONE_COLOUR, FONT

pygame.font.init()

class Board:
    size = 6
    cell_size = SCREEN_SIZE[0] // size

    def __init__(self):
        self.board = [[0]*Board.size for _ in range(Board.size)]
        self.sum_board = [[0]*Board.size for _ in range(Board.size)]
        self.stone_size = Board.cell_size // 2
        self.num = 2

    def neighbour_sum(self):
        sums = {}
        for row in range(Board.size):
            for col in range(Board.size):
                if self.board[row][col]: continue
                sum = 0
                for i in range(-1, 2): # Loop through neighbours 
                    for j in range(-1, 2):
                        if row+i < 0 or col+j < 0: continue
                        try: sum += self.board[row+i][col+j]
                        except: continue
                if sum > 1: 
                    if sum not in sums:
                        sums[sum] = set()
                    sums[sum].add((row, col))
        return sums
    
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
                    else: print(f"\033[97m{self.sum_board[row][col]}\033[00m", end=" ")
                else: print(0, end=" ")
            print()
        print()

    def place_stone(self, pos, num=None):
        sums = self.neighbour_sum()
        if not self.board[pos[0]][pos[1]]: 
            if self.num == 1: 
                self.board[pos[0]][pos[1]] = 1
            if num: 
                self.board[pos[0]][pos[1]] = num
            elif self.num in sums and pos in sums[self.num]: 
                self.board[pos[0]][pos[1]] = self.num
                self.num += 1
        self.draw_sum_board(self.neighbour_sum())

    def draw_board(self, screen):
        screen.fill(COLOUR_ONE)
        for row in range(Board.size):
            for col in range(row % 2, Board.size, 2):
                pygame.draw.rect(screen, COLOUR_TWO, (col*Board.cell_size, row*Board.cell_size, Board.cell_size, Board.cell_size))
    
    def draw(self, screen):
        self.draw_board(screen)
        for row in range(Board.size):
            for col in range(Board.size):
                if self.board[row][col] != 0:
                    cpos = (row*Board.cell_size + self.stone_size, col*Board.cell_size + self.stone_size, )

                    gfxdraw.aacircle(screen, cpos[1], cpos[0], self.stone_size - 10, STONE_COLOUR)
                    gfxdraw.filled_circle(screen, cpos[1], cpos[0], self.stone_size - 10, STONE_COLOUR)

                    number = FONT.render(f"{self.board[row][col]}", True, (0,0,0))
                    rect = number.get_rect()
                    rect.centery, rect.centerx = cpos
                    screen.blit(number, rect)


