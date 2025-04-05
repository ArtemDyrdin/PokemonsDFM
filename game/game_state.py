from pokemon import Pokemon

class GameState:
    def __init__(self):
        self.level = 30
        self.reset_game()
        
    def reset_game(self):
        """Сброс состояния игры для новой битвы"""
        self.pokemons = [
            Pokemon('Bulbasaur', self.level, 25, 150),
            Pokemon('Charmander', self.level, 175, 150),
            Pokemon('Squirtle', self.level, 325, 150)
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
    game_state.player1_pokemon.hp_x, game_state.player1_pokemon.hp_y = 275, 250
    game_state.player2_pokemon.hp_x, game_state.player2_pokemon.hp_y = 50, 50
    
    game_state.player1_pokemon.x = 0
    game_state.player1_pokemon.y = 100
    game_state.player1_pokemon.size = 300
    
    game_state.player2_pokemon.x = 250
    game_state.player2_pokemon.y = 0
    game_state.player2_pokemon.size = 300
    
    game_state.player1_pokemon.set_moves()
    game_state.player2_pokemon.set_moves()