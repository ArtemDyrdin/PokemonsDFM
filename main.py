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

def main():
    game_state = GameState()
    
    # Главный игровой цикл
    while game_state.status != 'quit':
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                game_state.status = 'quit'
            elif event.type == KEYDOWN:
                if event.key == K_y and game_state.status == 'gameover':
                    game_state.reset_game()
                elif event.key == K_n and game_state.status == 'gameover':
                    game_state.status = 'quit'
            elif event.type == MOUSEBUTTONDOWN:
                mouse_click = event.pos
                if game_state.status in ['select pokemon 1', 'select pokemon 2']:
                    handle_pokemon_selection(game_state, mouse_click, current_time)
                elif game_state.status == 'player 1 turn' or game_state.status == 'player 1 move':
                    handle_player_turn(game, game_state, mouse_click, current_time, 1)
                elif game_state.status == 'player 2 turn' or game_state.status == 'player 2 move':
                    handle_player_turn(game, game_state, mouse_click, current_time, 2)
        
        # Отрисовка игры
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