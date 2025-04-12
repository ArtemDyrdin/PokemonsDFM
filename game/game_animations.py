import pygame
import time


from constants import *
from ui import display_message, create_button



battle_surf_flag = 0
battle_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

font_path2 = "res/pokemon_fire_red.ttf"
font_path = "res/rus3.ttf"

def init_resources():
    global battlefields_img, menubar1_img, menubar2_img, fightbackground_img, hpbar1_img, hpbar2_img
    battlefields_img = battlefields_img.convert_alpha()
    menubar1_img = menubar1_img.convert_alpha()
    menubar2_img = menubar2_img.convert_alpha()
    fightbackground_img = fightbackground_img.convert_alpha()
    hpbar1_img = hpbar1_img.convert_alpha()
    hpbar2_img = hpbar2_img.convert_alpha()



battlefields_img = pygame.image.load("res/battle_back.png")
battlefields_img = pygame.transform.scale(battlefields_img,(1200,561))

menubar1_img =  pygame.image.load("res/menubar1.png")
menubar1_img = pygame.transform.scale(menubar1_img,(1200,240))

menubar2_img =  pygame.image.load("res/menubar2.png")
menubar2_img = pygame.transform.scale(menubar2_img,(600,240))

fightbackground_img = pygame.image.load("res/fightbackground.png")
fightbackground_img = pygame.transform.scale(fightbackground_img,(1920,1280))

hpbar1_img = pygame.image.load("res/hp_bar1.png")
hpbar1_img = pygame.transform.scale(hpbar1_img,(520,186))

hpbar2_img = pygame.image.load("res/hp_bar2.png")
hpbar2_img = pygame.transform.scale(hpbar2_img,(510,149))



def fade_in_pokemon(pokemon, game, message):
    """Анимация постепенного появления покемона"""
    alpha = 0
    while alpha < 255:
        pokemon.draw(game, alpha)
        display_message(message, game)
        alpha += 0.4
        pygame.display.update()

def draw_message(game_state, game):
    """Отображает текущее сообщение в верхней части экрана"""
    if game_state.message and pygame.time.get_ticks() < game_state.message_timer:
        # Создаем полупрозрачный фон для сообщения
        s = pygame.Surface((GAME_WIDTH, 30))
        s.set_alpha(200)
        s.fill(WHITE)
        game.blit(s, (0, 0))
        # Рисуем текст сообщения
        font = pygame.font.Font(font_path, 28)
        text = font.render(game_state.message, True, BLACK)
        game.blit(text, (GAME_WIDTH//2 - text.get_width()//2, 5))

def draw_selection_screen(game_state, game):
    """Отрисовка экрана выбора покемона"""
    font = pygame.font.Font(font_path, 100)
    text = font.render('Выбери своего покемона', True, BLACK)
    game.blit(text, (GAME_WIDTH//2 - text.get_width()//2, 200))
    
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
    
    
    name1_font = pygame.font.Font(font_path, 90) #150 было 
    
    if game_state.player1_pokemon.name == "Bulbasaur":
        name1_text = name1_font.render("Физтрон", True, BLACK) 
    elif game_state.player1_pokemon.name == "Charmander":
        name1_text = name1_font.render("Филинарий", True, BLACK) 
    elif game_state.player1_pokemon.name == "Squirtle":
        name1_text = name1_font.render("Матультор", True, BLACK) 
        
    if game_state.player2_pokemon.name == "Bulbasaur":
        name2_text = name1_font.render("Физтрон", True, BLACK) 
    elif game_state.player2_pokemon.name == "Charmander":
        name2_text = name1_font.render("Филинарий", True, BLACK) 
    elif game_state.player2_pokemon.name == "Squirtle":
        name2_text = name1_font.render("Матультор", True, BLACK) 
    
        
        
# =============================================================================
#     name1_text = name1_font.render(f"{game_state.player1_pokemon.name}", True, BLACK) 
#     name2_text = name1_font.render(f"{game_state.player2_pokemon.name}", True, BLACK) 
#     
# =============================================================================
   # game.blit(title_text, (GAME_WIDTH//2 - title_text.get_width()//2, GAME_HEIGHT//5))
    
    global battle_surf_flag
    
    if(battle_surf_flag == 0):
        battle_surf.blit(fightbackground_img,(0,0))
        battle_surf.blit(battlefields_img,(360,180))
        battle_surf.blit(menubar1_img,(360,180+561))
        battle_surf.blit(menubar2_img,(960,180+561))
        game_state.player1_pokemon.draw(battle_surf)
        game_state.player2_pokemon.draw(battle_surf)
        battle_surf.blit(hpbar1_img,(970, 550)) 
        battle_surf.blit(hpbar2_img,(550, 250)) 
        game_state.player1_pokemon.draw_hp(battle_surf)
        game_state.player2_pokemon.draw_hp(battle_surf)
        battle_sufr_flag = 1
        
    game.blit(battle_surf,(0,0))
    
    
    game.blit(name2_text, (580, 245))
    game.blit(name1_text, (1040, 550))
        

    
    # Отрисовка сообщения
    draw_message(game_state, game)
    
    # Определение текущего состояния для отрисовки UI
    if 'turn' in game_state.status or 'move' in game_state.status:
        player_num = 1 if '1' in game_state.status else 2
        
        # Отображение подсказки
        font = pygame.font.Font(font_path, 96)
        action = "Выберите атака" if 'move' in game_state.status else "Выберите действие"
        text = font.render(f"Ход {player_num}-го игрока - {action}", True, BLACK)
        game.blit(text, (500, 100))
        
        # Кнопки для выбора действия
        if 'turn' in game_state.status:
            pokemon = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
            game_state.fight_button = create_button(240, 70, 1000, 825, 130, 385, 'Атака', game)
            game_state.potion_button = create_button(240, 70, 1250, 825, 370, 385, f'Зелье ({pokemon.num_potions})', game)
        
        # Кнопки атак
        elif 'move' in game_state.status:
            pokemon = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
            game_state.move_buttons = [
                create_button(240, 70, 1000 + i % 2 * 240, 790 + i // 2 * 70, 
                             120 + i % 2 * 240, 385 + i // 2 * 70, 
                             move.name.capitalize(), game)
                for i, move in enumerate(pokemon.moves)
            ]
        
       # pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)
