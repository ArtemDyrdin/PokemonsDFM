from pokemon import Pokemon
import json

class GameState:
    def __init__(self):
        self.level = 30
        self.reset_game()
        
    def reset_game(self):
        """Сброс состояния игры для новой битвы"""
        # Загрузка данных из JSON-файла
        with open('pokemons-info.json', 'r',encoding='utf-8') as file:
            data = json.load(file)

        self.pokemons = [
            Pokemon('Bulbasaur', self.level, 25, 150, data),
            Pokemon('Charmander', self.level, 175, 150, data),
            Pokemon('Squirtle', self.level, 325, 150, data)
        ]
        self.player1_pokemon = None
        self.player2_pokemon = None
        self.current_player = None
        self.message = ""
        self.message_timer = 0
        self.status = 'select pokemon 1'
        self.move_buttons = []
        self.fight_button = None
        self.potion_button = None

def init_battle_positions(game_state):
    """Устанавливает позиции покемонов для битвы"""
    game_state.player1_pokemon.hp_x, game_state.player1_pokemon.hp_y = 1208, 636
    game_state.player2_pokemon.hp_x, game_state.player2_pokemon.hp_y = 755, 340
    
    game_state.player1_pokemon.x = 520
    game_state.player1_pokemon.y = 460
    game_state.player1_pokemon.size = 300
    
    game_state.player2_pokemon.x = 1100
    game_state.player2_pokemon.y = 220
    game_state.player2_pokemon.size = 300
    
    game_state.player1_pokemon.set_moves()
    game_state.player2_pokemon.set_moves()