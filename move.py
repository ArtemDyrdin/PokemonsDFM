# move.py

class Move:
    def __init__(self, data):
        '''Загрузка названия, силы и типа атаки покемона'''
        self.name = data['Name']
        self.power = data['Power']
        self.type = data['Type']