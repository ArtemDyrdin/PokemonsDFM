import pygame
from pygame.locals import *
import time
from constants import *
from ui import display_message
from game.game_state import GameState
from game.game_animations import fade_in_pokemon, draw_battle_ui, draw_message, draw_selection_screen, init_resources
from game.game_logic import handle_player_turn, handle_pokemon_selection, handle_fainted_state

pygame.init()

# Установка игрового окна
game = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Pokemon Battle')

init_resources()

menu_back = pygame.image.load("res/start.png").convert_alpha()


button_img = pygame.image.load("res/button_img.png").convert_alpha()
button_img = pygame.transform.scale(button_img,(500,178))

button2_img = pygame.image.load("res/button2_img.png").convert_alpha()
button2_img = pygame.transform.scale(button_img,(500,178))


stat_img = pygame.image.load("res/stat_nice.png").convert_alpha()
stat_img = pygame.transform.scale(stat_img,(1100,651))

left_arr_img = pygame.image.load("res/left_arr.png").convert_alpha()
left_arr_img = pygame.transform.scale(left_arr_img,(115,178))

right_arr_img = pygame.image.load("res/right_arr.png").convert_alpha()
right_arr_img = pygame.transform.scale(right_arr_img,(115,178))

battlefields_img = pygame.image.load("res/battle_back.png").convert_alpha()
battlefields_img = pygame.transform.scale(battlefields_img,(1200,561))

menubar1_img =  pygame.image.load("res/menubar1.png").convert_alpha()
menubar1_img = pygame.transform.scale(menubar1_img,(1200,240))

menubar2_img =  pygame.image.load("res/menubar2.png").convert_alpha()
menubar2_img = pygame.transform.scale(menubar2_img,(600,240))

fightbackground_img = pygame.image.load("res/fightbackground.png").convert_alpha()
fightbackground_img = pygame.transform.scale(fightbackground_img,(1920,1280))

pygame.event.set_allowed([pygame.QUIT, MOUSEBUTTONDOWN,KEYDOWN])



def draw_main_menu():
    
    game.blit(menu_back,(0,0))
    
    # Рисуем заголовок
    title_font = pygame.font.Font(font_path2, 195) #150 было 
    title_text = title_font.render("Pokemon Battle", True, WHITE) #Pokemon Battle
    title_text_shade = title_font.render("Pokemon Battle", True,BLACK)
    game.blit(title_text_shade, (GAME_WIDTH//2 - title_text.get_width()//2 + 5, GAME_HEIGHT//5 + 5))
    game.blit(title_text, (GAME_WIDTH//2 - title_text.get_width()//2, GAME_HEIGHT//5))
    
    # Рисуем кнопки
    button_font = pygame.font.Font(font_path, 136) # 96 
    
    # Кнопка для файтинга
    fight_button = pygame.Rect(GAME_WIDTH//2-250, GAME_HEIGHT//2-100, 500, 178)
    #pygame.draw.rect(game,RED,fight_button)
    fight_text = button_font.render("В бой", True, WHITE)
    fight_text_shade = button_font.render("В бой", True, (107,107,106))
    game.blit(button_img,(GAME_WIDTH//2-250, GAME_HEIGHT//2-100))
    game.blit(fight_text_shade, (fight_button.centerx-fight_text.get_width()//2 + 4, fight_button.centery-fight_text.get_height()//1.3 + 3))
    game.blit(fight_text, (fight_button.centerx-fight_text.get_width()//2, fight_button.centery-fight_text.get_height()//1.3))
    
    # Кнопка для просмотра характеристик
    view_button = pygame.Rect(GAME_WIDTH//2-250, GAME_HEIGHT//1.45-100, 500, 178)
    #pygame.draw.rect(game, BLUE, view_button)
    view_text = button_font.render("Покемоны", True, WHITE)
    view_text_shade = button_font.render("Покемоны", True, (107,107,106))
    game.blit(button_img,(GAME_WIDTH//2-250, GAME_HEIGHT//1.45-100))
    game.blit(view_text_shade, (view_button.centerx-view_text.get_width()//2 + 4, view_button.centery-view_text.get_height()//1.3 + 3))
    game.blit(view_text, (view_button.centerx-view_text.get_width()//2, view_button.centery-view_text.get_height()//1.3))

    return fight_button, view_button

def draw_pokemon_stats(game_state, current_pokemon_index):
    
    
    game.blit(menu_back,(0,0))
    game.blit(stat_img,(GAME_WIDTH//2 - 550, GAME_HEIGHT//2 - 410))
    
    
    # Получаем текущего покемона
    pokemon = game_state.pokemons[current_pokemon_index]
    
    # Сохраняем оригинальные координаты
    original_x, original_y = pokemon.x, pokemon.y
    
    # Временно меняем координаты для отрисовки
    pokemon.x, pokemon.y = GAME_WIDTH//4+45, 200
    pokemon.draw(game)  # Теперь будет рисоваться в новых координатах
    
    # Восстанавливаем оригинальные координаты
    pokemon.x, pokemon.y = original_x, original_y
    
    # Рисуем характеристики
    font = pygame.font.Font(font_path, 112)
    desk_font = pygame.font.Font(font_path, 65)
    
    # Имя покемона
    if(pokemon.name == "Bulbasaur"):
        
        name_text = font.render("Физтрон", True, BLACK)
        name_text_2 = font.render("Физтрон", True, WHITE)
        name_text_shade = font.render("Физтрон", True, (216,216,192))
        
        game.blit(name_text, (684 - name_text.get_width()//2+4  , 105+3))
        game.blit(name_text_2, (684 - name_text.get_width()//2 , 105))
        
        description_text1 = desk_font.render("Он создан в высокоэнергетической лаборатории. Способен", True, BLACK)
        description_text2 = desk_font.render("разгонятся до невероятных скоростей, вызывая электрические", True, BLACK)
        description_text3 = desk_font.render("всплески.", True, BLACK)
        game.blit(description_text1, (450, 570))
        game.blit(description_text2, (450, 635))
        game.blit(description_text3, (450, 700))
        
        #419+265 GAME_WIDTH//2-12
        
        game.blit(name_text_shade, (1180 +4 , 113 + 3))
        game.blit(name_text, (1180, 113))
        
    elif(pokemon.name == "Charmander"):
        
        name_text = font.render("Филинарий", True, BLACK)
        name_text_2 = font.render("Филинарий", True, WHITE)
        name_text_shade = font.render("Филинарий", True, (216,216,192))
        
        game.blit(name_text, (684 - name_text.get_width()//2+4  , 105+4))
        game.blit(name_text_2, (684 - name_text.get_width()//2 , 105))
        
        #419+265 GAME_WIDTH//2-12
        
        description_text1 = desk_font.render("Древний покемон, напоминающий сову, встроенную в античную", True, BLACK)
        description_text2 = desk_font.render("колонну. Способен передавать знания телепатически и является", True, BLACK)
        description_text3 = desk_font.render("тем, кто заблудился в раздумьях.", True, BLACK)
        game.blit(description_text1, (450, 570))
        game.blit(description_text2, (450, 635))
        game.blit(description_text3, (450, 700))
        
        game.blit(name_text_shade, (1180 +4 , 113 + 4))
        game.blit(name_text, (1180, 113))
        
    elif(pokemon.name == "Squirtle"):
        
        name_text = font.render("Матультор", True, BLACK)
        name_text_2 = font.render("Матультор", True, WHITE)
        name_text_shade = font.render("Матультор", True, (216,216,192))
        
        game.blit(name_text, (684 - name_text.get_width()//2+4  , 105+4))
        game.blit(name_text_2, (684 - name_text.get_width()//2 , 105))
        
        description_text1 = desk_font.render("Главный фокусник сея физмата. Он может, нажав на кнопку,", True, BLACK)
        description_text2 = desk_font.render("немного видеоизменять пространство, например, размеры", True, BLACK)
        description_text3 = desk_font.render("других покемонов.", True, BLACK)
        game.blit(description_text1, (450, 570))
        game.blit(description_text2, (450, 635))
        game.blit(description_text3, (450, 700))
        
        #419+265 GAME_WIDTH//2-12
        
        game.blit(name_text_shade, (1180 +4 , 113 + 4))
        game.blit(name_text, (1180, 113))
    
    # Характеристики
    hp_text = font.render(f"{pokemon.max_hp}", True, BLACK)
    hp_text_shade = font.render(f"{pokemon.max_hp}", True, (216,216,192))
    game.blit(hp_text, (1340, 195))
    
    attack_text = font.render(f"{pokemon.attack}", True, BLACK)
    attack_text_shade = font.render(f"{pokemon.attack}", True, (216,216,192))
    game.blit(attack_text, (1340, 255))
    
    defense_text = font.render(f"{pokemon.defense}", True, BLACK)
    degense_text_shade = font.render(f"{pokemon.defense}", True, (216,216,192))
    game.blit(defense_text, (1340, 313))
    
    speed_text = font.render(f"{pokemon.speed}", True, BLACK)
    game.blit(speed_text, (1340, 372))
    
    
    #Описание 
    description_text = font.render("Древний покемон, напоминающий сову", True, BLACK)
    game.blit(speed_text, (1340, 372))
    

    if(len(pokemon.types)) == 2:
        font2 = pygame.font.Font(font_path, 70)
        type_text = font2.render(f"{pokemon.types[0]},{pokemon.types[1]}", True, BLACK)
        game.blit(type_text , (1265, 455))
    else: 
        font2 = pygame.font.Font(font_path, 112)
        type_text = font2.render(f"{pokemon.types[0]}", True, BLACK)
        game.blit(type_text , (1378-type_text.get_width()//2, 430))
       


    # Кнопки навигации
    back_button = pygame.Rect(GAME_WIDTH//2 - 250, GAME_HEIGHT//1.2-110, 500, 178)
    #pygame.draw.rect(game, GREY, back_button)
    game.blit(button_img,(GAME_WIDTH//2 - 250, GAME_HEIGHT//1.2-110))
    back_text = font.render("Назад", True, WHITE)
    back_text_shade = font.render("Назад", True, (107,107,106))
    game.blit(back_text_shade, (back_button.centerx-back_text.get_width()//2 + 4, back_button.centery-back_text.get_height()//1.3 + 3))
    game.blit(back_text, (back_button.centerx-back_text.get_width()//2, back_button.centery-back_text.get_height()//1.3))
    
    prev_button = pygame.Rect(GAME_WIDTH//2 - 450, GAME_HEIGHT//1.2-110, 115, 178)
   # pygame.draw.rect(game, BLUE, prev_button)
    #prev_text = font.render("<", True, WHITE)
    game.blit(left_arr_img, (GAME_WIDTH//2 - 450, GAME_HEIGHT//1.2-110))
   # game.blit(prev_text, (275 - prev_text.get_width()//2, 365))
    
    next_button = pygame.Rect(GAME_WIDTH//2 + 355, GAME_HEIGHT//1.2-110, 115, 178)
   # pygame.draw.rect(game, BLUE, next_button)
    game.blit(right_arr_img, (GAME_WIDTH//2 + 355, GAME_HEIGHT//1.2-110))
   # next_text = font.render(">", True, WHITE)
    #game.blit(next_text, (375 - next_text.get_width()//2, 365))
    
    return back_button, prev_button, next_button



def draw_gameover_buttons(surface):
    """Отрисовка кнопок для экрана завершения игры и возврат их Rect"""
    button_width = 500  # Увеличим размер кнопок для удобства
    button_height = 178
    spacing = 20
    
    # Кнопка "Играть снова"
    replay_btn = pygame.Rect(
        GAME_WIDTH//2 - button_width - spacing//2,
        GAME_HEIGHT//2 - button_height//2,
        button_width,
        button_height
    )
    pygame.draw.rect(surface, (0,0,0,0), replay_btn)  # Прозрачный фон
    game.blit(button_img, (replay_btn.x, replay_btn.y))
    
    # Кнопка "Выход"
    quit_btn = pygame.Rect(
        GAME_WIDTH//2 + spacing//2,
        GAME_HEIGHT//2 - button_height//2,
        button_width,
        button_height
    )
    pygame.draw.rect(surface, (0,0,0,0), quit_btn)
    game.blit(button_img, (quit_btn.x, quit_btn.y))
    
    # Текст на кнопках
    font = pygame.font.Font(font_path, 96)
    replay_text = font.render("Play Again", True, WHITE)
    quit_text = font.render("Main Menu", True, WHITE)
    
    surface.blit(replay_text, (replay_btn.x + 50, replay_btn.y + 50))
    surface.blit(quit_text, (quit_btn.x + 50, quit_btn.y + 50))
    
    return replay_btn, quit_btn

def main():
    game_state = GameState()
    current_mode = "main_menu"  # Возможные значения: "main_menu", "fight", "view_stats"
    current_pokemon_index = 0  # Для режима просмотра характеристик
    gameover_buttons_surface = None
    gameover_buttons = None
    
    
    # Главный игровой цикл
    while game_state.status != 'quit':
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                game_state.status = 'quit'
                
        
            
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_click = event.pos
                
                if current_mode == "main_menu":
                    fight_button, view_button = draw_main_menu()
                    if fight_button.collidepoint(mouse_click):
                       # game.blit(button_img,(GAME_WIDTH//2-250, GAME_HEIGHT//2-100))
                       
                        current_mode = "fight"
                        game_state.status = "select pokemon 1"
                    elif view_button.collidepoint(mouse_click):
                        current_mode = "view_stats"
                
                elif current_mode == "view_stats":
                    back_button, prev_button, next_button = draw_pokemon_stats(game_state, current_pokemon_index)
                    if back_button.collidepoint(mouse_click):
                        current_mode = "main_menu"
                    elif prev_button.collidepoint(mouse_click):
                        current_pokemon_index = (current_pokemon_index - 1) % len(game_state.pokemons)
                    elif next_button.collidepoint(mouse_click):
                        current_pokemon_index = (current_pokemon_index + 1) % len(game_state.pokemons)
                
                elif current_mode == "fight":
                    if game_state.status in ['select pokemon 1', 'select pokemon 2']:
                        handle_pokemon_selection(game_state, mouse_click, current_time)
                    elif game_state.status == 'player 1 turn' or game_state.status == 'player 1 move':
                        handle_player_turn(game, game_state, mouse_click, current_time, 1)
                    elif game_state.status == 'player 2 turn' or game_state.status == 'player 2 move':
                        handle_player_turn(game, game_state, mouse_click, current_time, 2)
            
            elif event.type == KEYDOWN:
                if event.key == K_y and game_state.status == 'gameover':
                    game_state.reset_game()
                    current_mode = "main_menu"
                elif event.key == K_n and game_state.status == 'gameover':
                    game_state.status = 'quit'
                elif current_mode == "view_stats":
                    if event.key == K_LEFT:
                        current_pokemon_index = (current_pokemon_index - 1) % len(game_state.pokemons)
                    elif event.key == K_RIGHT:
                        current_pokemon_index = (current_pokemon_index + 1) % len(game_state.pokemons)
                    elif event.key == K_ESCAPE:
                        current_mode = "main_menu"
        # Отрисовка игры
        if current_mode == "main_menu":
            draw_main_menu()
        
        elif current_mode == "view_stats":
            draw_pokemon_stats(game_state, current_pokemon_index)
        
        elif current_mode == "fight":
            game.blit(menu_back,(0,0))
            
            if game_state.status in ['select pokemon 1', 'select pokemon 2']:
                draw_selection_screen(game_state, game)
            
            elif game_state.status == 'prebattle':
                #game_state.player1_pokemon.draw(game)
                #draw_message(game_state, game)
                #pygame.display.update()
                game_state.status = 'start battle'
                
               
            
            elif game_state.status == 'start battle':
                               
                game.blit(fightbackground_img,(0,0))
                game.blit(battlefields_img,(360,180))
                game.blit(menubar1_img,(360,180+561))
                game.blit(menubar2_img,(960,180+561))     
                
# =============================================================================
#                 fade_in_pokemon(game_state.player2_pokemon, game, f'Player 2 sent out {game_state.player2_pokemon.name}!')
#                 fade_in_pokemon(game_state.player1_pokemon, game, f'Player 1 sent out {game_state.player1_pokemon.name}!')
# =============================================================================
                
                game_state.player1_pokemon.draw_hp(game)
                game_state.player2_pokemon.draw_hp(game)
                
                # Определяем кто ходит первым по скорости
                game_state.status = 'player 2 turn' if game_state.player2_pokemon.speed > game_state.player1_pokemon.speed else 'player 1 turn'
                pygame.display.update()
                
            
            elif game_state.status in ['player 1 turn', 'player 2 turn', 'player 1 move', 'player 2 move']:
                draw_battle_ui(game_state, game)
            
            elif game_state.status == 'fainted':
                handle_fainted_state(game_state, game)

            elif game_state.status == 'gameover':
                
                game_state.status = "main_menu"
                game_state.reset_game()
                current_mode = "main_menu"

        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()