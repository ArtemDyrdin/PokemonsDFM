import pygame
from pygame.locals import *
import time
import random
from constants import *
from pokemon import Pokemon
from ui import display_message, create_button

pygame.init()

# Установка игрового окна
game = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Pokemon Battle')

# Инициализация покемонов
level = 30
pokemons = [
    Pokemon('Bulbasaur', level, 25, 150),
    Pokemon('Charmander', level, 175, 150),
    Pokemon('Squirtle', level, 325, 150)
]

game_status = 'select pokemon 1'
player1_pokemon = None
player2_pokemon = None
current_player = None
message = ""
message_timer = 0

def draw_message():
    """Отображает текущее сообщение в верхней части экрана"""
    if message and pygame.time.get_ticks() < message_timer:
        # Создаем полупрозрачный фон для сообщения
        s = pygame.Surface((GAME_WIDTH, 30))
        s.set_alpha(200)
        s.fill(WHITE)
        game.blit(s, (0, 0))
        # Рисуем текст сообщения
        font = pygame.font.Font(None, 28)
        text = font.render(message, True, BLACK)
        game.blit(text, (GAME_WIDTH//2 - text.get_width()//2, 5))

# Главный игровой цикл
while game_status != 'quit':
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = 'quit'
        elif event.type == KEYDOWN:
            if event.key == K_y:
                # установка покемонов при повторе игры
                pokemons = [
                    Pokemon('Bulbasaur', level, 25, 150),
                    Pokemon('Charmander', level, 175, 150),
                    Pokemon('Squirtle', level, 325, 150)
                ]
                game_status = 'select pokemon 1'
                message = ""
            elif event.key == K_n:
                game_status = 'quit'
        elif event.type == MOUSEBUTTONDOWN:
            mouse_click = event.pos
            if game_status == 'select pokemon 1':
                # Выбор покемона для игрока 1
                for i, pokemon in enumerate(pokemons):
                    if pokemon.get_rect().collidepoint(mouse_click):
                        player1_pokemon = pokemon
                        # Удаляем выбранного покемона из списка доступных для игрока 2
                        remaining_pokemons = [p for j, p in enumerate(pokemons) if j != i]
                        pokemons = remaining_pokemons
                        game_status = 'select pokemon 2'
                        message = f"Player 1 selected {player1_pokemon.name}"
                        message_timer = current_time + 2000  # Показывать сообщение 2 секунды
            elif game_status == 'select pokemon 2':
                # Выбор покемона для игрока 2
                for i, pokemon in enumerate(pokemons):
                    if pokemon.get_rect().collidepoint(mouse_click):
                        player2_pokemon = pokemon
                        # Настройка позиций и параметров покемонов
                        player1_pokemon.hp_x, player1_pokemon.hp_y = 275, 250
                        player2_pokemon.hp_x, player2_pokemon.hp_y = 50, 50
                        game_status = 'prebattle'
                        message = f"Player 2 selected {player2_pokemon.name}"
                        message_timer = current_time + 2000
            elif game_status == 'player 1 turn':
                # Ход игрока 1
                if fight_button.collidepoint(mouse_click):
                    game_status = 'player 1 move'
                elif potion_button.collidepoint(mouse_click):
                    if player1_pokemon.num_potions == 0:
                        message = 'No more potions left'
                        message_timer = current_time + 2000
                    else:
                        player1_pokemon.use_potion()
                        message = f'Player 1: {player1_pokemon.name} used potion'
                        message_timer = current_time + 2000
                        game_status = 'player 2 turn'
            elif game_status == 'player 1 move':
                for i, button in enumerate(move_buttons):
                    if button.collidepoint(mouse_click):
                        move = player1_pokemon.moves[i]
                        player1_pokemon.perform_attack(player2_pokemon, move, game)
                        message = f"Player 1 used {move.name}!"
                        message_timer = current_time + 2000
                        game_status = 'player 2 turn' if player2_pokemon.current_hp > 0 else 'fainted'
            elif game_status == 'player 2 turn':
                # Ход игрока 2
                if fight_button.collidepoint(mouse_click):
                    game_status = 'player 2 move'
                elif potion_button.collidepoint(mouse_click):
                    if player2_pokemon.num_potions == 0:
                        message = 'No more potions left'
                        message_timer = current_time + 2000
                    else:
                        player2_pokemon.use_potion()
                        message = f'Player 2: {player2_pokemon.name} used potion'
                        message_timer = current_time + 2000
                        game_status = 'player 1 turn'
            elif game_status == 'player 2 move':
                for i, button in enumerate(move_buttons):
                    if button.collidepoint(mouse_click):
                        move = player2_pokemon.moves[i]
                        player2_pokemon.perform_attack(player1_pokemon, move, game)
                        message = f"Player 2 used {move.name}!"
                        message_timer = current_time + 2000
                        game_status = 'player 1 turn' if player1_pokemon.current_hp > 0 else 'fainted'

    # Отрисовка игры
    game.fill(WHITE)
    
    if game_status in ['select pokemon 1', 'select pokemon 2']:
        # Отображение заголовка
        font = pygame.font.Font(None, 36)
        if game_status == 'select pokemon 1':
            text = font.render('Player 1: Select your Pokemon', True, BLACK)
        else:
            text = font.render('Player 2: Select your Pokemon', True, BLACK)
        game.blit(text, (GAME_WIDTH//2 - text.get_width()//2, 20))
        
        for pokemon in pokemons:
            pokemon.draw(game)
        
        mouse_cursor = pygame.mouse.get_pos()
        for pokemon in pokemons:
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, BLACK, pokemon.get_rect(), 2)
        
        draw_message()
    
    elif game_status == 'prebattle':
        player1_pokemon.draw(game)
        draw_message()
        
        pygame.display.update()
        player1_pokemon.set_moves()
        player2_pokemon.set_moves()

        player1_pokemon.x = 0
        player1_pokemon.y = 100
        player1_pokemon.size = 300

        player2_pokemon.x = 250
        player2_pokemon.y = 0
        player2_pokemon.size = 300

        game_status = 'start battle'
        continue
    
    elif game_status == 'start battle':
        alpha = 0
        while alpha < 255:
            game.fill(WHITE)
            player2_pokemon.draw(game, alpha)
            display_message(f'Player 2 sent out {player2_pokemon.name}!', game)
            alpha += 0.4
            pygame.display.update()
        time.sleep(1)
        alpha = 0
        while alpha < 255:
            game.fill(WHITE)
            player2_pokemon.draw(game)
            player1_pokemon.draw(game, alpha)
            display_message(f'Player 1 sent out {player1_pokemon.name}!', game)
            alpha += 0.4
            pygame.display.update()
        
        player1_pokemon.draw_hp(game)
        player2_pokemon.draw_hp(game)

        # Определяем кто ходит первым по скорости
        game_status = 'player 2 turn' if player2_pokemon.speed > player1_pokemon.speed else 'player 1 turn'
        pygame.display.update()
        time.sleep(1)
        continue
    
    elif game_status in ['player 1 turn', 'player 2 turn', 'player 1 move', 'player 2 move']:
        # Отрисовка покемонов и их HP
        player1_pokemon.draw(game)
        player2_pokemon.draw(game)
        player1_pokemon.draw_hp(game)
        player2_pokemon.draw_hp(game)
        
        # Отрисовка сообщения
        draw_message()
        
        # Отрисовка интерфейса в зависимости от состояния
        if game_status == 'player 1 turn':
            # Отображение подсказки
            font = pygame.font.Font(None, 28)
            text = font.render("Player 1's turn - Choose action", True, BLACK)
            game.blit(text, (20, 300))
            
            # Кнопки
            fight_button = create_button(240, 70, 10, 350, 130, 385, 'Fight', game)
            potion_button = create_button(240, 70, 250, 350, 370, 385, f'Potion ({player1_pokemon.num_potions})', game)
        
        elif game_status == 'player 2 turn':
            # Отображение подсказки
            font = pygame.font.Font(None, 28)
            text = font.render("Player 2's turn - Choose action", True, BLACK)
            game.blit(text, (20, 300))
            
            # Кнопки
            fight_button = create_button(240, 70, 10, 350, 130, 385, 'Fight', game)
            potion_button = create_button(240, 70, 250, 350, 370, 385, f'Potion ({player2_pokemon.num_potions})', game)
        
        elif game_status == 'player 1 move':
            # Отображение подсказки
            font = pygame.font.Font(None, 28)
            text = font.render("Player 1: Choose a move", True, BLACK)
            game.blit(text, (20, 300))
            
            # Кнопки атак
            move_buttons = [
                create_button(240, 70, 10 + i % 2 * 240, 350 + i // 2 * 70, 120 + i % 2 * 240, 385 + i // 2 * 70, 
                             move.name.capitalize(), game)
                for i, move in enumerate(player1_pokemon.moves)
            ]
        
        elif game_status == 'player 2 move':
            # Отображение подсказки
            font = pygame.font.Font(None, 28)
            text = font.render("Player 2: Choose a move", True, BLACK)
            game.blit(text, (20, 300))
            
            # Кнопки атак
            move_buttons = [
                create_button(240, 70, 10 + i % 2 * 240, 350 + i // 2 * 70, 120 + i % 2 * 240, 385 + i // 2 * 70, 
                             move.name.capitalize(), game)
                for i, move in enumerate(player2_pokemon.moves)
            ]
        
        pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)
    
    elif game_status == 'fainted':
        alpha = 255
        while alpha > 0:
            game.fill(WHITE)
            player1_pokemon.draw_hp(game)
            player2_pokemon.draw_hp(game)
            if player2_pokemon.current_hp == 0:
                player1_pokemon.draw(game)
                player2_pokemon.draw(game, alpha)
                display_message(f'Player 2: {player2_pokemon.name} fainted!', game)
            else:
                player1_pokemon.draw(game, alpha)
                player2_pokemon.draw(game)
                display_message(f'Player 1: {player1_pokemon.name} fainted!', game)
            alpha -= 0.4
            pygame.display.update()
        game_status = 'gameover'
    
    elif game_status == 'gameover':
        if player2_pokemon.current_hp == 0:
            display_message('Player 1 wins! Play again (Y/N)?', game)
        else:
            display_message('Player 2 wins! Play again (Y/N)?', game)
    
    pygame.display.update()

pygame.quit()