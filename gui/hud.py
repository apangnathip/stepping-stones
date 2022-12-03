import pygame
from stepstone.constants import *


def display_text(screen, bound, margin, text, font, colour=(255,255,255)):
    text_surf = pygame.Surface(bound.size, pygame.SRCALPHA, 32).convert_alpha()
    words = text.split(" ")
    space_width, space_height = font.size(" ")
    pos = (margin, bound.height/2 - space_height/2)
    x, y = pos
    adjusted_height = 0
    for word in words:
        word_surf = font.render(word, True, colour)
        word_width, word_height = word_surf.get_size()
        if x + word_width >= bound.width - margin:
            x = pos[0]
            y += word_height
            adjusted_height -= word_height/2
        text_surf.blit(word_surf, (x, y))
        x += word_width + space_width
    screen.blit(text_surf, (bound.left, bound.top + adjusted_height))
    
# TODO SLIDER
class Button():
    def __init__(self, parent, label, align, relative_pos=0):
        self.label = label
        self.hover = False
        self.activated = True
        self.colour = BUTTON_COLOUR
        self.act_colour = BUTTON_ACT_COLOUR
        self.draw_label = True
        
        if align == "top":
            self.rect = pygame.Rect(
                parent.x_pos + parent.hud_margin + (parent.button_width + parent.button_margin) * relative_pos, 
                MARGIN + parent.button_margin, 
                parent.button_width,
                parent.button_height
            )
        elif align == "bottom":
            self.rect = pygame.Rect(
                parent.x_pos + parent.hud_margin + (parent.button_width + parent.button_margin) * relative_pos, 
                parent.ctrl_y_pos + parent.button_margin, 
                parent.button_width,
                parent.button_height
            )
    
    def draw(self, screen):
        if not self.activated: return
        
        if self.hover:
            button_colour = self.act_colour
            hud_font_colour = HUD_ACT_FONT_COLOUR
        else: 
            button_colour = self.colour
            hud_font_colour = HUD_FONT_COLOUR

        pygame.draw.rect(screen, button_colour, self.rect)

        if not self.draw_label: return
        label_surf = HUD_FONT.render(self.label, True, hud_font_colour)
        label_rect = label_surf.get_rect()
        screen.blit(label_surf, (self.rect.centerx - label_rect.width/2, self.rect.centery - label_rect.height/2, 0, 0))

class Slider(Button):
    def __init__(self, parent, label, align):
        super().__init__(parent, label, align)
        self.draw_label = False
        self.slider_rect = parent.slider_rect
        self.rect.width /= 8
        self.rect.height -= 20
        self.min = self.slider_rect.left
        self.max = self.slider_rect.left + self.slider_rect.width
        self.rect.center = (self.min + (self.max - self.min)/2, parent.slider_y_pos - parent.button_height/2)
        self.colour = (0, 0, 0)
        self.toggle = False


class Hud():
    def __init__(self, board):
        self.board_num = board.num
        self.width = SCREEN_SIZE[0] - (board.rendered_size + MARGIN * 2) - MARGIN
        self.height = SCREEN_SIZE[1] - MARGIN * 2
        # self.height = board.rendered_size
        self.hud_margin = 15

        self.x_pos = board.rendered_size + MARGIN * 2
        self.ctrl_y_pos = MARGIN + self.height - CTRLBAR_SIZE
        self.button_margin = 15
        self.button_width = (self.width - self.hud_margin*2 -  self.button_margin*3) / 4
        self.button_height = CTRLBAR_SIZE - self.button_margin*2

        self.slider_size = CTRLBAR_SIZE/24
        self.slider_y_pos = self.ctrl_y_pos - self.slider_size
        self.slider_rect = pygame.Rect(self.x_pos + self.hud_margin*8, self.ctrl_y_pos - CTRLBAR_SIZE/3 - self.slider_size/2, self.width/1.5, self.slider_size)

    def draw(self, screen, board):
        pygame.draw.rect(screen, HUD_COLOUR, (self.x_pos, MARGIN, self.width, self.height))
  
        info_text = pygame.Rect(self.x_pos, MARGIN, self.width, CTRLBAR_SIZE)
        pygame.draw.rect(screen, CTRLBAR_COLOUR, info_text)
        if board.solving == "loud":
            info = f"Finding optimal solution, at branch #{board.branch_num}"
        elif board.highest_num and board.num > board.highest_num: 
            info = f"The highest possible stone of degree {board.highest_num} has been achieved!"
        else: 
            info = f"Placing {board.num}'s stone..."
        display_text(screen, info_text, self.hud_margin*2, info, HUD_FONT)

        size_rect = pygame.Rect(self.x_pos, self.ctrl_y_pos - CTRLBAR_SIZE/1.5, self.width, CTRLBAR_SIZE/1.5)
        pygame.draw.rect(screen, HUD_COLOUR_SEC, size_rect)
        display_text(screen, size_rect, self.hud_margin*2, "Size :", HUD_FONT)
        # slider_rect = pygame.Rect(self.x_pos + self.hud_margin*8, self.ctrl_y_pos - size_rect.height/2 - self.slider_size/2, self.width/1.5, self.slider_size)
        pygame.draw.rect(screen, HUD_FONT_COLOUR, self.slider_rect)
        
        pygame.draw.rect(screen, CTRLBAR_COLOUR, (self.x_pos, self.ctrl_y_pos, self.width, CTRLBAR_SIZE))

