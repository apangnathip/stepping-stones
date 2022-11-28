import pygame
from stepstone.constants import *

class Button():
    def __init__(self, parent, label, align, relative_pos=0):
        self.label = label
        self.hover = False
        self.activated = True

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
            button_colour = BUTTON_ACT_COLOUR
            hud_font_colour = HUD_ACT_FONT_COLOUR
        else: 
            button_colour = BUTTON_COLOUR
            hud_font_colour = HUD_FONT_COLOUR

        pygame.draw.rect(screen, button_colour, self.rect)
        label_surf = HUD_FONT.render(self.label, True, hud_font_colour)
        label_rect = label_surf.get_rect()
        screen.blit(label_surf, (self.rect.centerx - label_rect.width/2, self.rect.centery - label_rect.height/2, 0, 0))

class Hud():
    def __init__(self, board):
        self.board_num = board.num
        self.width = SCREEN_SIZE[0] - (board.rendered_size + MARGIN * 2) - MARGIN
        self.height = SCREEN_SIZE[1] - MARGIN * 2
        self.x_pos = board.rendered_size + MARGIN * 2
        self.ctrl_y_pos = MARGIN + self.height - CTRLBAR_SIZE
        self.hud_margin = 15
        self.buttons_num = 4
        self.button_margin = 15
        self.button_width = (self.width - self.hud_margin*2 -  self.button_margin*3) / 4
        self.button_height = CTRLBAR_SIZE - self.button_margin*2
        self.buttons = []

    def draw(self, screen, board):
        pygame.draw.rect(screen, HUD_COLOUR, (self.x_pos, MARGIN, self.width, self.height))

        pygame.draw.rect(screen, CTRLBAR_COLOUR, (self.x_pos, MARGIN, self.width, CTRLBAR_SIZE))
        info_text = HUD_FONT.render(f"Placing {board.num}'s Stones...", True, HUD_FONT_COLOUR)
        info_rect = info_text.get_rect()
        screen.blit(info_text, (self.x_pos + self.hud_margin*2, MARGIN + self.hud_margin + info_rect.height/2, info_rect.width, info_rect.height))

        pygame.draw.rect(screen, CTRLBAR_COLOUR, (self.x_pos, self.ctrl_y_pos, self.width, CTRLBAR_SIZE))
        for button in self.buttons: 
            button.draw()
