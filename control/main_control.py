import serial
import serial.tools.list_ports

import pygame
from pygame.locals import *

from game.game_state import init_battle_positions

# Инициализация последовательного порта для Arduino
def init_serial(virtual_joystick):
    try:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Arduino" in port.description or "CH340" in port.description:
                try:
                    ser = serial.Serial(port.device, 9600, timeout=0.1)
                    print(f"Connected to Arduino on {port.device}")
                    return ser
                except:
                    continue
        print("Arduino not found! Using keyboard controls")
        return virtual_joystick  # Возвращаем виртуальный джойстик вместо None
    except Exception as e:
        print(f"Error during serial init: {e}")
        return virtual_joystick

def handle_arduino_input(game_state, current_mode, current_pokemon_index, player1_selection, player2_selection, selection_cooldown, ser, virtual_joystick, KEYBOARD_JOYSTICK_MAPPING, game):
    
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
                                button, game_state, current_mode, current_pokemon_index, player1_selection, game)
                        else:
                            current_mode, current_pokemon_index = handle_player2_input(
                                button, game_state, current_mode, current_pokemon_index, player2_selection, game)
            except UnicodeDecodeError:
                continue  # Пропускаем битые данные
            except Exception as e:
                print(f"Ошибка обработки данных: {e}")
                continue
    
    except Exception as e:
        print(f"Ошибка в работе с последовательным портом: {e}")
        # Можно добавить попытку переподключения здесь
    
    return current_mode, current_pokemon_index

def handle_player1_input(button, game_state, current_mode, current_pokemon_index, player1_selection, game):
    
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

def handle_player2_input(button, game_state, current_mode, current_pokemon_index, player2_selection, game):
    
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