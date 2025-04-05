import pygame
import time

from constants import *
from ui import display_message, create_button

def fade_in_pokemon(pokemon, game, message):
    """Анимация постепенного появления покемона"""
    alpha = 0
    while alpha < 255:
        game.fill(WHITE)
        pokemon.draw(game, alpha)
        display_message(message, game)
        alpha += 0.4
        pygame.display.update()
    time.sleep(1)

def draw_message(game_state, game):
    """Отображает текущее сообщение в верхней части экрана"""
    if game_state.message and pygame.time.get_ticks() < game_state.message_timer:
        # Создаем полупрозрачный фон для сообщения
        s = pygame.Surface((GAME_WIDTH, 30))
        s.set_alpha(200)
        s.fill(WHITE)
        game.blit(s, (0, 0))
        # Рисуем текст сообщения
        font = pygame.font.Font(None, 28)
        text = font.render(game_state.message, True, BLACK)
        game.blit(text, (GAME_WIDTH//2 - text.get_width()//2, 5))

def draw_selection_screen(game_state, game):
    """Отрисовка экрана выбора покемона"""
    font = pygame.font.Font(None, 36)
    text = font.render(f'Player {1 if game_state.status == "select pokemon 1" else 2}: Select your Pokemon', True, BLACK)
    game.blit(text, (GAME_WIDTH//2 - text.get_width()//2, 20))
    
    for pokemon in game_state.pokemons:
        pokemon.draw(game)
    
    mouse_cursor = pygame.mouse.get_pos()
    for pokemon in game_state.pokemons:
        if pokemon.get_rect().collidepoint(mouse_cursor):
            pygame.draw.rect(game, BLACK, pokemon.get_rect(), 2)
    
    draw_message(game_state, game)

def draw_battle_ui(game_state, game):
    """Отрисовка интерфейса битвы"""
    # Отрисовка покемонов и их HP
    game_state.player1_pokemon.draw(game)
    game_state.player2_pokemon.draw(game)
    game_state.player1_pokemon.draw_hp(game)
    game_state.player2_pokemon.draw_hp(game)
    
    # Отрисовка сообщения
    draw_message(game_state, game)
    
    # Определение текущего состояния для отрисовки UI
    if 'turn' in game_state.status or 'move' in game_state.status:
        player_num = 1 if '1' in game_state.status else 2
        
        # Отображение подсказки
        font = pygame.font.Font(None, 28)
        action = "Choose a move" if 'move' in game_state.status else "Choose action"
        text = font.render(f"Player {player_num}'s turn - {action}", True, BLACK)
        game.blit(text, (20, 300))
        
        # Кнопки для выбора действия
        if 'turn' in game_state.status:
            pokemon = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
            game_state.fight_button = create_button(240, 70, 10, 350, 130, 385, 'Fight', game)
            game_state.potion_button = create_button(240, 70, 250, 350, 370, 385, f'Potion ({pokemon.num_potions})', game)
        
        # Кнопки атак
        elif 'move' in game_state.status:
            pokemon = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
            game_state.move_buttons = [
                create_button(240, 70, 10 + i % 2 * 240, 350 + i // 2 * 70, 
                             120 + i % 2 * 240, 385 + i // 2 * 70, 
                             move.name.capitalize(), game)
                for i, move in enumerate(pokemon.moves)
            ]
        
        pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)
