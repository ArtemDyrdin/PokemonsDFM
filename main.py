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


def draw_gameover_buttons(game):
    """Отрисовка кнопок для экрана завершения игры (однократная)"""
    # Создаем поверхность для кнопок
    buttons_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    
    button_width = 200
    button_height = 60
    spacing = 20
    
    # Кнопка "Играть снова"
    replay_btn = pygame.Rect(
        GAME_WIDTH//2 - button_width - spacing//2,
        GAME_HEIGHT//2 - button_height//2,
        button_width,
        button_height
    )
    pygame.draw.rect(buttons_surface, GREEN, replay_btn)
    
    # Кнопка "Выход"
    quit_btn = pygame.Rect(
        GAME_WIDTH//2 + spacing//2,
        GAME_HEIGHT//2 - button_height//2,
        button_width,
        button_height
    )
    pygame.draw.rect(buttons_surface, RED, quit_btn)
    
    # Текст на кнопках
    font = pygame.font.Font(None, 36)
    replay_text = font.render("Play Again", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    
    # Позиционирование текста
    buttons_surface.blit(replay_text, (
        replay_btn.x + (button_width - replay_text.get_width())//2,
        replay_btn.y + (button_height - replay_text.get_height())//2
    ))
    
    buttons_surface.blit(quit_text, (
        quit_btn.x + (button_width - quit_text.get_width())//2,
        quit_btn.y + (button_height - quit_text.get_height())//2
    ))
    
    # Отрисовываем поверхность с кнопками на основном экране
    game.blit(buttons_surface, (0, 0))
    
    return replay_btn, quit_btn


def main():
    game_state = GameState()
    current_mode = "main_menu"  # Возможные значения: "main_menu", "fight", "view_stats"
    current_pokemon_index = 0  # Для режима просмотра характеристик
    gameover_buttons = None  # Для хранения кнопок завершения игры
    main_menu_buttons = None  # Добавим переменную для хранения кнопок главного меню
    selection_handled = False  # Флаг для отслеживания обработки выбора
    gameover_buttons_surface = None
    
    # Главный игровой цикл
    while game_state.status != 'quit':
        current_time = pygame.time.get_ticks()
        game.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                game_state.status = 'quit'
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_click = event.pos

                if game_state.status == 'gameover' and gameover_buttons:
                    replay_btn, quit_btn = gameover_buttons
                    if replay_btn.collidepoint(mouse_click):
                        game_state.reset_game()
                        current_mode = "fight"
                        game_state.status = "select pokemon 1"
                        selection_handled = False  # Сброс флага
                        gameover_buttons_surface = None  # Важно: сбрасываем поверхность
                        gameover_buttons = None
                    elif quit_btn.collidepoint(mouse_click):
                        game_state.status = 'main_menu'
                        current_mode = "main_menu"
                
                elif current_mode == "main_menu":
                    main_menu_buttons = draw_main_menu()
                    if main_menu_buttons:
                        fight_button, view_button = main_menu_buttons
                        if fight_button.collidepoint(mouse_click):
                            current_mode = "fight"
                            game_state.status = "select pokemon 1"
                            selection_handled = False
                
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
                        # Обработка выбора покемона с защитой от повторной обработки
                        if not selection_handled:
                            prev_status = game_state.status
                            handle_pokemon_selection(game_state, mouse_click, current_time)
                            if prev_status != game_state.status:
                                selection_handled = True
                    elif game_state.status in ['player 1 turn', 'player 1 move']:
                        # Обработка хода игрока 1
                        handle_player_turn(game, game_state, mouse_click, current_time, 1)
                        selection_handled = False  # Сброс после обработки хода
                    elif game_state.status in ['player 2 turn', 'player 2 move']:
                        # Обработка хода игрока 2
                        handle_player_turn(game, game_state, mouse_click, current_time, 2)
                        selection_handled = False  # Сброс после обработки хода
                    else:
                        selection_handled = False  # Сброс для других состояний
            
            elif event.type == KEYDOWN:
                if current_mode == "view_stats":
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
                selection_handled = False  # Сброс флага после отрисовки
            
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
                continue
            
            elif game_state.status in ['player 1 turn', 'player 2 turn', 'player 1 move', 'player 2 move']:
                draw_battle_ui(game_state, game)
            
            elif game_state.status == 'fainted':
                handle_fainted_state(game_state, game)

            elif game_state.status == 'gameover':
                if gameover_buttons_surface is None:
                    # Создаем поверхность для всего экрана завершения один раз
                    gameover_buttons_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
                    gameover_buttons_surface.fill(WHITE)
                    
                    # Отрисовываем текст результата
                    result_text = "Player 1 wins!" if game_state.player2_pokemon.current_hp == 0 else "Player 2 wins!"
                    display_message(result_text, gameover_buttons_surface)
                    
                    # Отрисовываем кнопки
                    replay_btn, quit_btn = draw_gameover_buttons(gameover_buttons_surface)
                    gameover_buttons = (replay_btn, quit_btn)
                
                # Отображаем готовую поверхность
                game.blit(gameover_buttons_surface, (0, 0))
                    
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()