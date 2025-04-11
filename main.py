import pygame
from pygame.locals import *
import time
from constants import *
from ui import display_message
from game.game_state import GameState
from game.game_animations import fade_in_pokemon, draw_battle_ui, draw_message, draw_selection_screen
from game.game_logic import handle_player_turn, handle_pokemon_selection, handle_fainted_state

pygame.init()

# Установка игрового окна
game = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Pokemon Battle')

#менюшка
menu_back = pygame.image.load("res/start.png") 

button_img = pygame.image.load("res/button_img.png")
button_img = pygame.transform.scale(button_img,(500,178))

font_path2 = "res/pokemon_fire_red.ttf"
font_path = "res/rus3.ttf"

stat_img = pygame.image.load("res/stat_back.png")
stat_img = pygame.transform.scale(stat_img,(1500,561))

left_arr_img = pygame.image.load("res/left_arr.png")
left_arr_img = pygame.transform.scale(left_arr_img,(115,178))

right_arr_img = pygame.image.load("res/right_arr.png")
right_arr_img = pygame.transform.scale(right_arr_img,(115,178))




def draw_main_menu():
    game.fill(WHITE)
    game.blit(menu_back,(0,0))
    
    game.fill(WHITE)
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
    pygame.draw.rect(game,RED,fight_button)
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
    game.fill(WHITE)
    game.blit(menu_back,(0,0))
    game.blit(stat_img,(GAME_WIDTH//2 - 750, GAME_HEIGHT//2-320))
    
    
    # Получаем текущего покемона
    pokemon = game_state.pokemons[current_pokemon_index]
    
    # Сохраняем оригинальные координаты
    original_x, original_y = pokemon.x, pokemon.y
    
    # Временно меняем координаты для отрисовки
    pokemon.x, pokemon.y = GAME_WIDTH//5-10, 340
    pokemon.draw(game)  # Теперь будет рисоваться в новых координатах
    
    # Восстанавливаем оригинальные координаты
    pokemon.x, pokemon.y = original_x, original_y
    
    # Рисуем характеристики
    font = pygame.font.Font(font_path, 140)
    
    # Имя покемона
    name_text = font.render(f"{pokemon.name}", True, BLACK)
    name_text_2 = font.render(f"{pokemon.name}", True, WHITE)
    name_text_shade = font.render(f"{pokemon.name}", True, (216,216,192))
    game.blit(name_text, (GAME_WIDTH//5+30+4 , 200+4))
    game.blit(name_text_2, (GAME_WIDTH//5+30 , 200))
    game.blit(name_text_shade, (1285 +4 , 305 + 4))
    game.blit(name_text, (1285, 305))
    
    # Характеристики
    hp_text = font.render(f"{pokemon.max_hp}", True, BLACK)
    hp_text_shade = font.render(f"{pokemon.max_hp}", True, (216,216,192))
    game.blit(hp_text, (1400, 207))
    
    attack_text = font.render(f"{pokemon.attack}", True, BLACK)
    attack_text_shade = font.render(f"{pokemon.attack}", True, (216,216,192))
    game.blit(attack_text, (1500, 417))
    
    defense_text = font.render(f"{pokemon.defense}", True, BLACK)
    degense_text_shade = font.render(f"{pokemon.defense}", True, (216,216,192))
    game.blit(defense_text, (1500, 527))
    
    speed_text = font.render(f"{pokemon.speed}", True, BLACK)
    game.blit(speed_text, (1500, 637))
    
    # Кнопки навигации
    back_button = pygame.Rect(GAME_WIDTH//2 - 250, GAME_HEIGHT//1.2-110, 500, 178)
    #pygame.draw.rect(game, GREY, back_button)
    game.blit(button_img,(GAME_WIDTH//2 - 250, GAME_HEIGHT//1.2-110))
    back_text = font.render("Back", True, WHITE)
    back_text_shade = font.render("Back", True, (107,107,106))
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

def main():
    game_state = GameState()
    current_mode = "main_menu"  # Возможные значения: "main_menu", "fight", "view_stats"
    current_pokemon_index = 0  # Для режима просмотра характеристик
    
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
            game.fill(WHITE)
            game.blit(menu_back,(0,0))
            
            if game_state.status in ['select pokemon 1', 'select pokemon 2']:
                draw_selection_screen(game_state, game)
            
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
                
                # Определяем кто ходит первым по скорости
                game_state.status = 'player 2 turn' if game_state.player2_pokemon.speed > game_state.player1_pokemon.speed else 'player 1 turn'
                pygame.display.update()
                time.sleep(1)
                continue
            
            elif game_state.status in ['player 1 turn', 'player 2 turn', 'player 1 move', 'player 2 move']:
                draw_battle_ui(game_state, game)
            
            elif game_state.status == 'fainted':
                handle_fainted_state(game_state, game)
            
            elif game_state.status == 'gameover':
                if game_state.player2_pokemon.current_hp == 0:
                    display_message('Player 1 wins! Play again (Y/N)?', game)
                else:
                    display_message('Player 2 wins! Play again (Y/N)?', game)
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()