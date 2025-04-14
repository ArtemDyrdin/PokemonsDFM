# ui.py
import pygame
from constants import *



def display_message(message, game):
    '''Отображает сообщение в нижней части экрана'''
   # pygame.draw.rect(game, WHITE, (720, 350, 480, 140))
   # pygame.draw.rect(game, BLACK, (720, 350, 480, 140), 3)
    font = pygame.font.Font(font_path, 60)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect()
    text_rect.x = 720 - 60
    text_rect.y = 440
    game.blit(text, text_rect)
    pygame.display.update()

def create_button(width, height, left, top, text_cx, text_cy, label, game):
    '''Создает кнопку с текстом'''
    mouse_cursor = pygame.mouse.get_pos()
    button = pygame.Rect(left, top, width, height)
    if button.collidepoint(mouse_cursor):
        pygame.draw.rect(game, GOLD, button)
    else:
        pygame.draw.rect(game, (248,248,248), button)
    font = pygame.font.Font(font_path, 85)
    text = font.render(f'{label}', True, BLACK)
    text_rect = text.get_rect(center=(left+120, top+text.get_height()//3))
    game.blit(text, text_rect)
    return button
