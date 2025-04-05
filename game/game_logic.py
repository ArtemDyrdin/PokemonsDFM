import pygame

from constants import *
from game.game_state import init_battle_positions
from ui import display_message

def handle_pokemon_selection(game_state, mouse_click, current_time):
    """Обработка выбора покемона игроками"""
    if game_state.status == 'select pokemon 1':
        for i, pokemon in enumerate(game_state.pokemons):
            if pokemon.get_rect().collidepoint(mouse_click):
                game_state.player1_pokemon = pokemon
                game_state.pokemons = [p for j, p in enumerate(game_state.pokemons) if j != i]
                game_state.status = 'select pokemon 2'
                game_state.message = f"Player 1 selected {game_state.player1_pokemon.name}"
                game_state.message_timer = current_time + 2000
                return True
    
    elif game_state.status == 'select pokemon 2':
        for i, pokemon in enumerate(game_state.pokemons):
            if pokemon.get_rect().collidepoint(mouse_click):
                game_state.player2_pokemon = pokemon
                init_battle_positions(game_state)
                game_state.status = 'prebattle'
                game_state.message = f"Player 2 selected {game_state.player2_pokemon.name}"
                game_state.message_timer = current_time + 2000
                return True
    return False

def handle_player_turn(game, game_state, mouse_click, current_time, player_num):
    """Обработка хода игрока (выбор действия или атаки)"""
    if game_state.status == f'player {player_num} turn':
        if game_state.fight_button.collidepoint(mouse_click):
            game_state.status = f'player {player_num} move'
        elif game_state.potion_button.collidepoint(mouse_click):
            pokemon = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
            if pokemon.num_potions == 0:
                game_state.message = 'No more potions left'
                game_state.message_timer = current_time + 2000
            else:
                pokemon.use_potion()
                game_state.message = f'Player {player_num}: {pokemon.name} used potion'
                game_state.message_timer = current_time + 2000
                game_state.status = f'player {2 if player_num == 1 else 1} turn'
    
    elif game_state.status == f'player {player_num} move':
        for i, button in enumerate(game_state.move_buttons):
            if button.collidepoint(mouse_click):
                attacker = game_state.player1_pokemon if player_num == 1 else game_state.player2_pokemon
                defender = game_state.player2_pokemon if player_num == 1 else game_state.player1_pokemon
                move = attacker.moves[i]
                attacker.perform_attack(defender, move, game)
                game_state.message = f"Player {player_num} used {move.name}!"
                game_state.message_timer = current_time + 2000
                game_state.status = f'player {2 if player_num == 1 else 1} turn' if defender.current_hp > 0 else 'fainted'

def handle_fainted_state(game_state, game):
    """Обработка состояния, когда покемон падает в обморок"""
    alpha = 255
    while alpha > 0:
        game.fill(WHITE)
        game_state.player1_pokemon.draw_hp(game)
        game_state.player2_pokemon.draw_hp(game)
        
        if game_state.player2_pokemon.current_hp == 0:
            game_state.player1_pokemon.draw(game)
            game_state.player2_pokemon.draw(game, alpha)
            display_message(f'Player 2: {game_state.player2_pokemon.name} fainted!', game)
        else:
            game_state.player1_pokemon.draw(game, alpha)
            game_state.player2_pokemon.draw(game)
            display_message(f'Player 1: {game_state.player1_pokemon.name} fainted!', game)
        
        alpha -= 0.4
        pygame.display.update()
    
    game_state.status = 'gameover'