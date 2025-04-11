import pygame
from pygame.locals import *
import time
from constants import *
from ui import display_message
from game.game_state import GameState
from game.game_state import init_battle_positions
from game.game_animations import fade_in_pokemon, draw_battle_ui, draw_message, draw_selection_screen
from game.game_logic import handle_player_turn, handle_pokemon_selection, handle_fainted_state

from control.virtual_joystick import KEYBOARD_JOYSTICK_MAPPING, VirtualJoystick
from control.main_control import init_serial

pygame.init()

# Инициализация виртуального джойстика
virtual_joystick = VirtualJoystick()

ser = init_serial(virtual_joystick)

# Установка игрового окна
game = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Pokemon Battle')

def draw_main_menu():
    game.fill(WHITE)
    
    # Рисуем заголовок
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("Pokemon Battle", True, BLACK)
    game.blit(title_text, (GAME_WIDTH//2 - title_text.get_width()//2, 100))
    
    # Рисуем кнопки
    button_font = pygame.font.Font(None, 36)
    
    # Кнопка для файтинга
    fight_button = pygame.Rect(GAME_WIDTH//2 - 150, 200, 300, 50)
    pygame.draw.rect(game, RED, fight_button)
    fight_text = button_font.render("Fight Mode", True, WHITE)
    game.blit(fight_text, (GAME_WIDTH//2 - fight_text.get_width()//2, 215))
    
    # Кнопка для просмотра характеристик
    view_button = pygame.Rect(GAME_WIDTH//2 - 150, 300, 300, 50)
    pygame.draw.rect(game, BLUE, view_button)
    view_text = button_font.render("View Pokemon Stats", True, WHITE)
    game.blit(view_text, (GAME_WIDTH//2 - view_text.get_width()//2, 315))
    
    return fight_button, view_button

def draw_pokemon_stats(game_state, current_pokemon_index):
    game.fill(WHITE)
    
    # Получаем текущего покемона
    pokemon = game_state.pokemons[current_pokemon_index]
    
    # Сохраняем оригинальные координаты
    original_x, original_y = pokemon.x, pokemon.y
    
    # Временно меняем координаты для отрисовки
    pokemon.x, pokemon.y = GAME_WIDTH//2 - 50, 100
    pokemon.draw(game)  # Теперь будет рисоваться в новых координатах
    
    # Восстанавливаем оригинальные координаты
    pokemon.x, pokemon.y = original_x, original_y
    
    # Рисуем характеристики
    font = pygame.font.Font(None, 36)
    
    # Имя покемона
    name_text = font.render(f"Name: {pokemon.name}", True, BLACK)
    game.blit(name_text, (50, 50))
    
    # Характеристики
    hp_text = font.render(f"HP: {pokemon.max_hp}", True, BLACK)
    game.blit(hp_text, (50, 100))
    
    attack_text = font.render(f"Attack: {pokemon.attack}", True, BLACK)
    game.blit(attack_text, (50, 150))
    
    defense_text = font.render(f"Defense: {pokemon.defense}", True, BLACK)
    game.blit(defense_text, (50, 200))
    
    speed_text = font.render(f"Speed: {pokemon.speed}", True, BLACK)
    game.blit(speed_text, (50, 250))
    
    # Кнопки навигации
    back_button = pygame.Rect(50, 350, 150, 50)
    pygame.draw.rect(game, GREY, back_button)
    back_text = font.render("Back", True, BLACK)
    game.blit(back_text, (125 - back_text.get_width()//2, 365))
    
    prev_button = pygame.Rect(250, 350, 50, 50)
    pygame.draw.rect(game, BLUE, prev_button)
    prev_text = font.render("<", True, WHITE)
    game.blit(prev_text, (275 - prev_text.get_width()//2, 365))
    
    next_button = pygame.Rect(350, 350, 50, 50)
    pygame.draw.rect(game, BLUE, next_button)
    next_text = font.render(">", True, WHITE)
    game.blit(next_text, (375 - next_text.get_width()//2, 365))
    
    return back_button, prev_button, next_button

# Глобальные переменные для управления джойстиком
player1_selection = 0  # Текущая выбранная опция для игрока 1
player2_selection = 0  # Текущая выбранная опция для игрока 2
selection_cooldown = 0  # Задержка между выборами

def handle_arduino_input(game_state, current_mode, current_pokemon_index):
    global player1_selection, player2_selection, selection_cooldown
    
    current_time = pygame.time.get_ticks()
    if current_time < selection_cooldown:
        return current_mode, current_pokemon_index
    
    # Проверяем, есть ли подключение к Arduino/virtual_joystick
    if ser is None:
        return current_mode, current_pokemon_index
    
    try:
        # Обработка виртуальных событий джойстика (если используется клавиатура)
        if ser == virtual_joystick:
            keys = pygame.key.get_pressed()
            for key, (command, state) in KEYBOARD_JOYSTICK_MAPPING.items():
                if keys[key]:
                    virtual_joystick.write(command + str(state))
                    # Добавляем событие отпускания кнопки
                    virtual_joystick.write(command + '0')
                    selection_cooldown = current_time + 200
        
        # Чтение данных из последовательного порта
        while ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if len(line) == 5:  # Формат: "P1B01" (Игрок 1, Кнопка 0, Состояние 1)
                    player = line[1]
                    button = int(line[3])
                    state = int(line[4])
                    
                    if state == 1:
                        selection_cooldown = current_time + 200
                        if player == '1':
                            current_mode, current_pokemon_index = handle_player1_input(
                                button, game_state, current_mode, current_pokemon_index)
                        else:
                            current_mode, current_pokemon_index = handle_player2_input(
                                button, game_state, current_mode, current_pokemon_index)
            except UnicodeDecodeError:
                continue  # Пропускаем битые данные
            except Exception as e:
                print(f"Ошибка обработки данных: {e}")
                continue
    
    except Exception as e:
        print(f"Ошибка в работе с последовательным портом: {e}")
        # Можно добавить попытку переподключения здесь
    
    return current_mode, current_pokemon_index

def handle_player1_input(button, game_state, current_mode, current_pokemon_index):
    global player1_selection
    
    if current_mode == "main_menu":
        if button == 4:  # Кнопка "Огонь"
            current_mode = "fight"
            game_state.status = "select pokemon 1"
    
    elif current_mode == "view_stats":
        if button == 0:  # Вверх
            current_pokemon_index = (current_pokemon_index - 1) % len(game_state.pokemons)
        elif button == 1:  # Вниз
            current_pokemon_index = (current_pokemon_index + 1) % len(game_state.pokemons)
        elif button == 4:  # Огонь (назад)
            current_mode = "main_menu"
    
    elif current_mode == "fight":
        if game_state.status == 'select pokemon 1':
            if button == 0:  # Вверх
                player1_selection = (player1_selection - 1) % len(game_state.pokemons)
            elif button == 1:  # Вниз
                player1_selection = (player1_selection + 1) % len(game_state.pokemons)
            elif button == 4:  # Огонь (выбор)
                game_state.player1_pokemon = game_state.pokemons[player1_selection]
                game_state.pokemons = [p for i, p in enumerate(game_state.pokemons) if i != player1_selection]
                game_state.status = 'select pokemon 2'
                game_state.message = f"Player 1 selected {game_state.player1_pokemon.name}"
                game_state.message_timer = pygame.time.get_ticks() + 2000
        
        elif game_state.status == 'player 1 turn':
            if button == 0:  # Вверх
                player1_selection = (player1_selection - 1) % 4
            elif button == 1:  # Вниз
                player1_selection = (player1_selection + 1) % 4
            elif button == 4:  # Огонь (подтверждение)
                if player1_selection == 0:  # Атака
                    game_state.status = 'player 1 move'
                elif player1_selection == 1:  # Зелье
                    if game_state.player1_pokemon.num_potions > 0:
                        game_state.player1_pokemon.use_potion()
                        game_state.message = 'Player 1 used potion'
                        game_state.message_timer = pygame.time.get_ticks() + 2000
                        game_state.status = 'player 2 turn'
        
        elif game_state.status == 'player 1 move':
            if button == 0:  # Вверх
                player1_selection = (player1_selection - 1) % len(game_state.player1_pokemon.moves)
            elif button == 1:  # Вниз
                player1_selection = (player1_selection + 1) % len(game_state.player1_pokemon.moves)
            elif button == 4:  # Огонь (подтверждение)
                attacker = game_state.player1_pokemon
                defender = game_state.player2_pokemon
                move = attacker.moves[player1_selection]
                attacker.perform_attack(defender, move, game)
                game_state.message = f"Player 1 used {move.name}!"
                game_state.message_timer = pygame.time.get_ticks() + 2000
                game_state.status = 'player 2 turn' if defender.current_hp > 0 else 'fainted'
                player1_selection = 0
    
    return current_mode, current_pokemon_index

def handle_player2_input(button, game_state, current_mode, current_pokemon_index):
    global player2_selection
    
    if current_mode == "fight":
        if game_state.status == 'select pokemon 2':
            if button == 0:  # Вверх
                player2_selection = (player2_selection - 1) % len(game_state.pokemons)
            elif button == 1:  # Вниз
                player2_selection = (player2_selection + 1) % len(game_state.pokemons)
            elif button == 4:  # Огонь (выбор)
                game_state.player2_pokemon = game_state.pokemons[player2_selection]
                init_battle_positions(game_state)
                game_state.status = 'prebattle'
                game_state.message = f"Player 2 selected {game_state.player2_pokemon.name}"
                game_state.message_timer = pygame.time.get_ticks() + 2000
        
        elif game_state.status == 'player 2 turn':
            if button == 0:  # Вверх
                player2_selection = (player2_selection - 1) % 4
            elif button == 1:  # Вниз
                player2_selection = (player2_selection + 1) % 4
            elif button == 4:  # Огонь (подтверждение)
                if player2_selection == 0:  # Атака
                    game_state.status = 'player 2 move'
                elif player2_selection == 1:  # Зелье
                    if game_state.player2_pokemon.num_potions > 0:
                        game_state.player2_pokemon.use_potion()
                        game_state.message = 'Player 2 used potion'
                        game_state.message_timer = pygame.time.get_ticks() + 2000
                        game_state.status = 'player 1 turn'
        
        elif game_state.status == 'player 2 move':
            if button == 0:  # Вверх
                player2_selection = (player2_selection - 1) % len(game_state.player2_pokemon.moves)
            elif button == 1:  # Вниз
                player2_selection = (player2_selection + 1) % len(game_state.player2_pokemon.moves)
            elif button == 4:  # Огонь (подтверждение)
                attacker = game_state.player2_pokemon
                defender = game_state.player1_pokemon
                move = attacker.moves[player2_selection]
                attacker.perform_attack(defender, move, game)
                game_state.message = f"Player 2 used {move.name}!"
                game_state.message_timer = pygame.time.get_ticks() + 2000
                game_state.status = 'player 1 turn' if defender.current_hp > 0 else 'fainted'
                player2_selection = 0
    
    return current_mode, current_pokemon_index

def draw_selection_arrows(game, selections, game_state):
    """Рисует выделение выбранных вариантов прямоугольниками"""
    if game_state.status == 'select pokemon 1':
        # Выделение для выбора покемона игроком 1
        x = 100 + player1_selection * 150
        y = 150
        pygame.draw.rect(game, RED, (x-10, y-10, 120, 180), 3, border_radius=5)
        
    elif game_state.status == 'select pokemon 2':
        # Выделение для выбора покемона игроком 2

        x = 100 + player2_selection * 150
        y = 150
        pygame.draw.rect(game, BLUE, (x-10, y-10, 120, 180), 3, border_radius=5)
        
    elif game_state.status == 'player 1 turn':
        # Выделение для меню действий игрока 1
        menu_x = 50
        menu_y = GAME_HEIGHT - 150
        
        if player1_selection == 0:  # FIGHT
            pygame.draw.rect(game, RED, (menu_x + 15, menu_y + 20, 120, 30), 3, border_radius=5)
        elif player1_selection == 1:  # POTION
            pygame.draw.rect(game, RED, (menu_x + 15, menu_y + 60, 120, 30), 3, border_radius=5)
        elif player1_selection == 2:  # SWAP
            pygame.draw.rect(game, RED, (menu_x + 160, menu_y + 20, 120, 30), 3, border_radius=5)
        elif player1_selection == 3:  # RUN
            pygame.draw.rect(game, RED, (menu_x + 160, menu_y + 60, 120, 30), 3, border_radius=5)
            
    elif game_state.status == 'player 2 turn':
        # Выделение для меню действий игрока 2
        menu_x = GAME_WIDTH - 350
        menu_y = GAME_HEIGHT - 150
        
        if player2_selection == 0:  # FIGHT
            pygame.draw.rect(game, BLUE, (menu_x + 15, menu_y + 20, 120, 30), 3, border_radius=5)
        elif player2_selection == 1:  # POTION
            pygame.draw.rect(game, BLUE, (menu_x + 15, menu_y + 60, 120, 30), 3, border_radius=5)
        elif player2_selection == 2:  # SWAP
            pygame.draw.rect(game, BLUE, (menu_x + 160, menu_y + 20, 120, 30), 3, border_radius=5)
        elif player2_selection == 3:  # RUN
            pygame.draw.rect(game, BLUE, (menu_x + 160, menu_y + 60, 120, 30), 3, border_radius=5)
            
    elif game_state.status == 'player 1 move':
        # Выделение для выбора атаки игроком 1
        move_x = GAME_WIDTH // 2 - 200
        move_y = GAME_HEIGHT - 110
        pygame.draw.rect(game, RED, (move_x + 15, move_y + player1_selection * 30, 370, 25), 3, border_radius=5)
        
    elif game_state.status == 'player 2 move':
        # Выделение для выбора атаки игроком 2
        move_x = GAME_WIDTH // 2 - 200
        move_y = GAME_HEIGHT - 110
        pygame.draw.rect(game, BLUE, (move_x + 15, move_y + player2_selection * 30, 370, 25), 3, border_radius=5)

def main():
    global player1_selection, player2_selection
    
    game_state = GameState()
    current_mode = "main_menu"
    current_pokemon_index = 0
    
    # Главный игровой цикл
    while game_state.status != 'quit':
        current_time = pygame.time.get_ticks()
        
        # Обработка ввода (основное изменение)
        current_mode, current_pokemon_index = handle_arduino_input(
            game_state, current_mode, current_pokemon_index)
    
        # Обработка событий Pygame (упрощенная версия)
        for event in pygame.event.get():
            if event.type == QUIT:
                game_state.status = 'quit'
            elif event.type == KEYDOWN:
                # Оставляем только спец. клавиши (Y/N для рестарта)
                if event.key == K_y and game_state.status == 'gameover':
                    game_state.reset_game()
                    current_mode = "main_menu"
                    player1_selection = player2_selection = 0  # Сброс выбора
                elif event.key == K_n and game_state.status == 'gameover':
                    game_state.status = 'quit'
        
        # Отрисовка игры
        if current_mode == "main_menu":
            draw_main_menu()
        
        elif current_mode == "view_stats":
            draw_pokemon_stats(game_state, current_pokemon_index)
        
        elif current_mode == "fight":
            game.fill(WHITE)
            
            if game_state.status in ['select pokemon 1', 'select pokemon 2']:
                draw_selection_screen(game_state, game)
                draw_selection_arrows(game, (player1_selection, player2_selection), game_state)
            
            elif game_state.status == 'prebattle':
                game_state.player1_pokemon.draw(game)
                draw_message(game_state, game)
                pygame.display.update()
                game_state.status = 'start battle'
                continue
            
            elif game_state.status == 'start battle':
                fade_in_pokemon(game_state.player2_pokemon, game, f'Player 2 sent out {game_state.player2_pokemon.name}!')
                fade_in_pokemon(game_state.player1_pokemon, game, f'Player 1 sent out {game_state.player1_pokemon.name}!')
                
                game_state.player1_pokemon.draw_hp(game)
                game_state.player2_pokemon.draw_hp(game)
                
                game_state.status = 'player 2 turn' if game_state.player2_pokemon.speed > game_state.player1_pokemon.speed else 'player 1 turn'
                pygame.display.update()
                time.sleep(1)
                continue
            
            elif game_state.status in ['player 1 turn', 'player 2 turn', 'player 1 move', 'player 2 move']:
                draw_battle_ui(game_state, game)
                draw_selection_arrows(game, (player1_selection, player2_selection), game_state)
            
            elif game_state.status == 'fainted':
                handle_fainted_state(game_state, game)
            
            elif game_state.status == 'gameover':
                if game_state.player2_pokemon.current_hp == 0:
                    display_message('Player 1 wins! Play again (Y/N)?', game)
                else:
                    display_message('Player 2 wins! Play again (Y/N)?', game)
        
        pygame.display.update()
    
    if ser is not None:
        ser.close()
    pygame.quit()

if __name__ == "__main__":
    main()