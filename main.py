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