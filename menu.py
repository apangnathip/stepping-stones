import pygame
from stepstone.constants import MENU_COLOUR, MENU_SIZE, MENU_FONT   
from stepstone.board import Board 

class Button:
    def __init__(self, label_text):
        self.label_text = label_text
        self.padding = 5
        self.hovered = False
        self.label = MENU_FONT.render(label_text, True, (0,0,0))
        self.w, self.h = MENU_FONT.size(label_text)
        self.padded_w = self.w + self.padding*2
        self.rect = pygame.Rect(0, 0, self.padded_w, self.h)

    def draw(self, screen, pos):
        if self.hovered:
            pygame.draw.rect(screen, (200,230,255), (pos, 0, self.padded_w, self.h))
        else: 
            pygame.draw.rect(screen, (255,255,255), (pos, 0, self.padded_w, self.h))
        self.rect.left = pos
        screen.blit(self.label, (pos + self.padding, 0))

class Menu:
    def __init__(self):
        self.width, self.height = MENU_SIZE
        self.colour = MENU_COLOUR
        self.margin = 5
        self.rect = pygame.Rect(0, 0, MENU_SIZE[0], MENU_SIZE[1])
        self.buttons = (
            Button("Reset"), 
            Button("Undo"), 
            Button("Search"),
        )
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        pos = self.margin
        for button in self.buttons:
            button.draw(screen, pos)
            pos += button.padded_w + self.margin