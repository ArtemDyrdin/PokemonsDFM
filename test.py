# import pygame
# from pygame.locals import *
# import time
# from constants import *
# from ui import display_message
# from game.game_state import GameState
# from game.game_animations import fade_in_pokemon, draw_battle_ui, draw_message, draw_selection_screen
# from game.game_logic import handle_player_turn, handle_pokemon_selection, handle_fainted_state

# pygame.init()

# # Установка игрового окна
# game = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
# pygame.display.set_caption('Pokemon Battle')
# def main():
#     game_state = GameState()
#     current_mode = "main_menu"  # Возможные значения: "main_menu", "fight", "view_stats"
#     current_pokemon_index = 0  # Для режима просмотра характеристик
    
#     # Главный игровой цикл
#     while game_state.status != 'quit':
#         current_time = pygame.time.get_ticks()
        
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 game_state.status = 'quit'
            
#             elif event.type == MOUSEBUTTONDOWN:
#                 mouse_click = event.pos
                
#                 if current_mode == "main_menu":
#                     fight_button, view_button = draw_main_menu()
#                     if fight_button.collidepoint(mouse_click):
#                         current_mode = "fight"
#                         game_state.status = "select pokemon 1"
#                     elif view_button.collidepoint(mouse_click):
#                         current_mode = "view_stats"
                
#                 elif current_mode == "view_stats":
#                     back_button, prev_button, next_button = draw_pokemon_stats(game_state, current_pokemon_index)
#                     if back_button.collidepoint(mouse_click):
#                         current_mode = "main_menu"
#                     elif prev_button.collidepoint(mouse_click):
#                         current_pokemon_index = (current_pokemon_index - 1) % len(game_state.pokemons)
#                     elif next_button.collidepoint(mouse_click):
#                         current_pokemon_index = (current_pokemon_index + 1) % len(game_state.pokemons)
                
#                 elif current_mode == "fight":
#                     if game_state.status in ['select pokemon 1', 'select pokemon 2']:
#                         handle_pokemon_selection(game_state, mouse_click, current_time)
#                     elif game_state.status == 'player 1 turn' or game_state.status == 'player 1 move':
#                         handle_player_turn(game, game_state, mouse_click, current_time, 1)
#                     elif game_state.status == 'player 2 turn' or game_state.status == 'player 2 move':
#                         handle_player_turn(game, game_state, mouse_click, current_time, 2)
            
#             elif event.type == KEYDOWN:
#                 if event.key == K_y and game_state.status == 'gameover':
#                     game_state.reset_game()
#                     current_mode = "main_menu"
#                 elif event.key == K_n and game_state.status == 'gameover':
#                     game_state.status = 'quit'
#                 elif current_mode == "view_stats":
#                     if event.key == K_LEFT:
#                         current_pokemon_index = (current_pokemon_index - 1) % len(game_state.pokemons)
#                     elif event.key == K_RIGHT:
#                         current_pokemon_index = (current_pokemon_index + 1) % len(game_state.pokemons)
#                     elif event.key == K_ESCAPE:
#                         current_mode = "main_menu"
        
#         # Отрисовка игры
#         if current_mode == "main_menu":
#             draw_main_menu()
        
#         elif current_mode == "view_stats":
#             draw_pokemon_stats(game_state, current_pokemon_index)
        
#         elif current_mode == "fight":
#             game.fill(WHITE)
            
#             if game_state.status in ['select pokemon 1', 'select pokemon 2']:
#                 draw_selection_screen(game_state, game)
            
#             elif game_state.status == 'prebattle':
#                 game_state.player1_pokemon.draw(game)
#                 draw_message(game_state, game)
#                 pygame.display.update()
#                 game_state.status = 'start battle'
#                 continue
            
#             elif game_state.status == 'start battle':
#                 fade_in_pokemon(game_state.player2_pokemon, game, f'Player 2 sent out {game_state.player2_pokemon.name}!')
#                 fade_in_pokemon(game_state.player1_pokemon, game, f'Player 1 sent out {game_state.player1_pokemon.name}!')
                
#                 game_state.player1_pokemon.draw_hp(game)
#                 game_state.player2_pokemon.draw_hp(game)
                
#                 # Определяем кто ходит первым по скорости
#                 game_state.status = 'player 2 turn' if game_state.player2_pokemon.speed > game_state.player1_pokemon.speed else 'player 1 turn'
#                 pygame.display.update()
#                 time.sleep(1)
#                 continue
            
#             elif game_state.status in ['player 1 turn', 'player 2 turn', 'player 1 move', 'player 2 move']:
#                 draw_battle_ui(game_state, game)
            
#             elif game_state.status == 'fainted':
#                 handle_fainted_state(game_state, game)
            
#             elif game_state.status == 'gameover':
#                 if game_state.player2_pokemon.current_hp == 0:
#                     display_message('Player 1 wins! Play again (Y/N)?', game)
#                 else:
#                     display_message('Player 2 wins! Play again (Y/N)?', game)
        
#         pygame.display.update()
    
#     pygame.quit()

# def handle_pokemon_selection(game_state, mouse_click, current_time):
#     """Обработка выбора покемона игроками"""
#     if game_state.status == 'select pokemon 1':
#         for i, pokemon in enumerate(game_state.pokemons):
#             if pokemon.get_rect().collidepoint(mouse_click):
#                 game_state.player1_pokemon = pokemon
#                 game_state.pokemons = [p for j, p in enumerate(game_state.pokemons) if j != i]
#                 game_state.status = 'select pokemon 2'
#                 game_state.message = f"Player 1 selected {game_state.player1_pokemon.name}"
#                 game_state.message_timer = current_time + 2000
#                 return True
    
#     elif game_state.status == 'select pokemon 2':
#         for i, pokemon in enumerate(game_state.pokemons):
#             if pokemon.get_rect().collidepoint(mouse_click):
#                 game_state.player2_pokemon = pokemon
#                 init_battle_positions(game_state)
#                 game_state.status = 'prebattle'
#                 game_state.message = f"Player 2 selected {game_state.player2_pokemon.name}"
#                 game_state.message_timer = current_time + 2000
#                 return True
#     return False

# def handle_player_turn(game, game_state, mouse_click, current_time, player_num):
#     """Обработка хода игрока (выбор действия или атаки)"""
#     if game_state.status == f'player {player_num} turn':
#         if game_state.fight_button.collidepoint(mouse_click):
#             game_state.status = f'player {player_num} move'
#         elif game_state.potion_button.collidepoint(mouse_click):
#             pokemon = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
#             if pokemon.num_potions == 0:
#                 game_state.message = 'No more potions left'
#                 game_state.message_timer = current_time + 2000
#             else:
#                 pokemon.use_potion()
#                 game_state.message = f'Player {player_num}: {pokemon.name} used potion'
#                 game_state.message_timer = current_time + 2000
#                 game_state.status = f'player {2 if player_num == 1 else 1} turn'
    
#     elif game_state.status == f'player {player_num} move':
#         for i, button in enumerate(game_state.move_buttons):
#             if button.collidepoint(mouse_click):
#                 attacker = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
#                 defender = game_state.player2_pokemon if player_num == 1 else game_state.player1_pokemon
#                 move = attacker.moves[i]
#                 attacker.perform_attack(defender, move, game)
#                 game_state.message = f"Player {player_num} used {move.name}!"
#                 game_state.message_timer = current_time + 2000
#                 game_state.status = f'player {2 if player_num == 1 else 1} turn' if defender.current_hp > 0 else 'fainted'

# if __name__ == "__main__":
#     main()
