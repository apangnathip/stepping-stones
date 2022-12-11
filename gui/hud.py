import pygame
from stepstone.constants import *

# Text wrapping
def display_text(screen, bound, margin, text, font, center=True, colour=HUD_FONT_COLOUR, highlight=None):
    text_surf = pygame.Surface(bound.size, pygame.SRCALPHA, 32).convert_alpha()
    words = text.split(" ")
    space_width, space_height = font.size(" ")
    if center:
        pos = margin, bound.height/2 - space_height/2
    else:
        pos = margin, margin
    x, y = pos
    adjusted_height = 0
    curr_colour = colour
    for word in words:
        if highlight:
            if word == words[highlight]:
                curr_colour = BOARD_COLOUR_TWO
            else: curr_colour = colour
        word_surf = font.render(word, True, curr_colour)
        word_width, word_height = word_surf.get_size()
        if x + word_width >= bound.width - margin:
            x = pos[0]
            y += word_height
            if center: adjusted_height -= word_height/2
        text_surf.blit(word_surf, (x, y))
        x += word_width + space_width
    screen.blit(text_surf, (bound.left, bound.top + adjusted_height))
    
    
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

        label_surf = HUD_FONT.render(self.label, True, hud_font_colour)
        label_rect = label_surf.get_rect()
        screen.blit(label_surf, (self.rect.centerx - label_rect.width/2, self.rect.centery - label_rect.height/2, 0, 0))

class Slider(Button):
    def __init__(self, parent, label, align):
        super().__init__(parent, label, align)
        self.slider_rect = parent.slider_rect
        self.rect.width /= 8
        self.rect.height -= 20
        self.min = self.slider_rect.left
        self.max = self.slider_rect.left + self.slider_rect.width
        self.colour = (200, 200, 200)
        self.toggle = False
        self.sizes = BOARD_SIZES
        self.notch_spacing = self.slider_rect.width / (len(self.sizes)-1)
        self.notches_pos = [self.slider_rect.left + self.notch_spacing*i for i in range(len(self.sizes))]
        self.rect.center = (self.notches_pos[0], parent.slider_y_pos - parent.button_height/2)
        self.notch_rect = pygame.Rect(0, self.rect.top + self.rect.height/4, self.slider_rect.height, self.rect.height/2)
        self.rect.centerx = self.notches_pos[2]

    def change_notch(self, mouse_pos, curr_size):
        for i, notch_pos in enumerate(self.notches_pos):
            if abs(mouse_pos - notch_pos) < self.notch_spacing / 2:
                self.rect.centerx = notch_pos
                if self.sizes[i] != curr_size: return self.sizes[i] 

    def draw(self, screen):
        if not self.activated: return
        
        if self.hover or self.toggle:
            button_colour = self.act_colour
        else: button_colour = self.colour

        for notch_pos in self.notches_pos:
            self.notch_rect.centerx = notch_pos
            pygame.draw.rect(screen, HUD_FONT_COLOUR, self.notch_rect)
        pygame.draw.rect(screen, button_colour, self.rect)

class Hud():
    def __init__(self, board):
        self.board_num = board.num
        self.width = SCREEN_SIZE[0] - (board.rendered_size + MARGIN * 2) - MARGIN
        self.height = SCREEN_SIZE[1] - MARGIN * 2
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
  
        state_text = pygame.Rect(self.x_pos, MARGIN, self.width, CTRLBAR_SIZE)
        pygame.draw.rect(screen, CTRLBAR_COLOUR, state_text)
        if board.solving == "loud":
            state = f"Finding optimal solution, at branch #{board.branch_num}"
        elif board.highest_num and board.num > board.highest_num: 
            state = f"The highest possible stone of degree {board.highest_num} has been achieved!"
        else: 
            state = f"Placing {board.num}'s stone..."
        display_text(screen, state_text, self.hud_margin*2, state, HUD_FONT)

        if board.num_reached and board.solving == "loud":
            info_text = pygame.Rect(self.x_pos, CTRLBAR_SIZE + MARGIN, self.width, self.height)
            info = "Number reached: " + " ".join([str(num) for num in sorted(board.num_reached)])
            display_text(screen,info_text, self.hud_margin*2, info, HUD_FONT, center=False, highlight=-1)

        size_rect = pygame.Rect(self.x_pos, self.ctrl_y_pos - CTRLBAR_SIZE/1.5, self.width, CTRLBAR_SIZE/1.5)
        pygame.draw.rect(screen, HUD_COLOUR, size_rect)
        display_text(screen, size_rect, self.hud_margin*2, "Size :", HUD_FONT)
        pygame.draw.rect(screen, HUD_FONT_COLOUR, self.slider_rect)
        
        pygame.draw.rect(screen, CTRLBAR_COLOUR, (self.x_pos, self.ctrl_y_pos, self.width, CTRLBAR_SIZE))

