# main.py
import pygame
from pygame.locals import *
import time
import random
from constants import *
from pokemon import Pokemon
from ui import display_message, create_button

pygame.init()

# Создание окна игры
game = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Pokemon Battle')

# Создание стартовых покемонов
level = 30
bulbasaur = Pokemon('Bulbasaur', level, 25, 150)
charmander = Pokemon('Charmander', level, 175, 150)
squirtle = Pokemon('Squirtle', level, 325, 150)
pokemons = [bulbasaur, charmander, squirtle]

# Выбор покемонов игрока и соперника
player_pokemon = None
rival_pokemon = None

# Основной игровой цикл
game_status = 'select pokemon'
while game_status != 'quit':
    for event in pygame.event.get():
        # кнопка QUIT
        if event.type == QUIT:
            game_status = 'quit'
        # зажата клавиша
        if event.type == KEYDOWN:
            if event.key == K_y:
                bulbasaur = Pokemon('Bulbasaur', level, 25, 150)
                charmander = Pokemon('Charmander', level, 175, 150)
                squirtle = Pokemon('Squirtle', level, 325, 150)
                pokemons = [bulbasaur, charmander, squirtle]
                game_status = 'select pokemon'
            elif event.key == K_n:
                game_status = 'quit'
        # клик мышкой
        if event.type == MOUSEBUTTONDOWN:
            mouse_click = event.pos
            # выбор покемона
            if game_status == 'select pokemon':
                for i in range(len(pokemons)):
                    if pokemons[i].get_rect().collidepoint(mouse_click):
                        player_pokemon = pokemons[i]
                        rival_pokemon = pokemons[(i + 1) % len(pokemons)]
                        rival_pokemon.level = int(rival_pokemon.level * .75)
                        player_pokemon.hp_x = 275
                        player_pokemon.hp_y = 250
                        rival_pokemon.hp_x = 50
                        rival_pokemon.hp_y = 50
                        game_status = 'prebattle'
            # при выборе действия покемона
            elif game_status == 'player turn':
                # если атака
                if fight_button.collidepoint(mouse_click):
                    game_status = 'player move'
                # если зелье
                if potion_button.collidepoint(mouse_click):
                    if player_pokemon.num_potions == 0:
                        display_message('No more potions left', game)
                        time.sleep(2)
                        game_status = 'player move'
                    else:
                        player_pokemon.use_potion()
                        display_message(f'{player_pokemon.name} used potion', game)
                        time.sleep(2)
                        game_status = 'rival turn'
            # при атаке покемона
            elif game_status == 'player move':
                for i in range(len(move_buttons)):
                    button = move_buttons[i]
                    if button.collidepoint(mouse_click):
                        move = player_pokemon.moves[i]
                        player_pokemon.perform_attack(rival_pokemon, move, game)
                        if rival_pokemon.current_hp == 0:
                            game_status = 'fainted'
                        else:
                            game_status = 'rival turn'

    # страница выбора покемона из перечисленных
    if game_status == 'select pokemon':
        game.fill(WHITE)
        bulbasaur.draw(game)
        charmander.draw(game)  
        squirtle.draw(game)  
        mouse_cursor = pygame.mouse.get_pos()
        for pokemon in pokemons:
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game, BLACK, pokemon.get_rect(), 2)
        pygame.display.update()

    # страница подготовки к бою и загрузка параметров покемонов
    if game_status == 'prebattle':
        game.fill(WHITE)
        player_pokemon.draw(game)  
        pygame.display.update()
        player_pokemon.set_moves()
        rival_pokemon.set_moves()
        player_pokemon.x = -50
        player_pokemon.y = 100
        rival_pokemon.x = 250
        rival_pokemon.y = -50
        player_pokemon.size = 300
        rival_pokemon.size = 300
        player_pokemon.set_sprite('back_default')
        rival_pokemon.set_sprite('front_default')
        game_status = 'start battle'

    # представление покемонов в начале игры
    # alpha - прозрачность покемона
    if game_status == 'start battle':
        alpha = 0
        while alpha < 255:
            game.fill(WHITE)
            rival_pokemon.draw(game, alpha)  
            display_message(f'Rival sent out {rival_pokemon.name}!', game)  
            alpha += .4
            pygame.display.update()
        time.sleep(1)
        alpha = 0
        while alpha < 255:
            game.fill(WHITE)
            rival_pokemon.draw(game)  
            player_pokemon.draw(game, alpha)  
            display_message(f'Go {player_pokemon.name}!', game)  
            alpha += .4
            pygame.display.update()
        player_pokemon.draw_hp(game)  
        rival_pokemon.draw_hp(game)  

        # начинает самый быстрый покемон
        if rival_pokemon.speed > player_pokemon.speed:
            game_status = 'rival turn'
        else:
            game_status = 'player turn'
        pygame.display.update()
        time.sleep(1)

    # выбор действия игрока
    if game_status == 'player turn':
        game.fill(WHITE)
        player_pokemon.draw(game)  
        rival_pokemon.draw(game)  
        player_pokemon.draw_hp(game)  
        rival_pokemon.draw_hp(game)  
        fight_button = create_button(240, 140, 10, 350, 130, 412, 'Fight', game)  
        potion_button = create_button(240, 140, 250, 350, 370, 412, f'Use Potion ({player_pokemon.num_potions})', game)  
        pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)
        pygame.display.update()

    # атака игрока
    if game_status == 'player move':
        game.fill(WHITE)
        player_pokemon.draw(game)  
        rival_pokemon.draw(game)  
        player_pokemon.draw_hp(game)  
        rival_pokemon.draw_hp(game)  
        move_buttons = []
        for i in range(len(player_pokemon.moves)):
            move = player_pokemon.moves[i]
            button_width = 240
            button_height = 70
            left = 10 + i % 2 * button_width
            top = 350 + i // 2 * button_height
            text_center_x = left + 120
            text_center_y = top + 35
            button = create_button(button_width, button_height, left, top, text_center_x, text_center_y, move.name.capitalize(), game)  
            move_buttons.append(button)
        pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)
        pygame.display.update()

    # атака противника
    if game_status == 'rival turn':
        game.fill(WHITE)
        player_pokemon.draw(game)  
        rival_pokemon.draw(game)  
        player_pokemon.draw_hp(game)  
        rival_pokemon.draw_hp(game)  
        display_message('', game)  
        time.sleep(2)
        move = random.choice(rival_pokemon.moves)
        rival_pokemon.perform_attack(player_pokemon, move, game)  
        if player_pokemon.current_hp == 0:
            game_status = 'fainted'
        else:
            game_status = 'player turn'
        pygame.display.update()

    # игрок побежден
    if game_status == 'fainted':
        alpha = 255
        while alpha > 0:
            game.fill(WHITE)
            player_pokemon.draw_hp(game)  
            rival_pokemon.draw_hp(game)  
            # побежден ли противник
            if rival_pokemon.current_hp == 0:
                player_pokemon.draw(game)  
                rival_pokemon.draw(game, alpha)  
                display_message(f'{rival_pokemon.name} fainted!', game)  
            else:
                player_pokemon.draw(game, alpha)  
                rival_pokemon.draw(game)  
                display_message(f'{player_pokemon.name} fainted!', game)  
            alpha -= .4
            pygame.display.update()
        game_status = 'gameover'

    # кто-то побежден
    if game_status == 'gameover':
        display_message('Play again (Y/N)?', game)  

pygame.quit()