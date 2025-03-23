# move.py
import requests

class Move:
    def __init__(self, url):
        '''Загрузка названия, силы и типа атаки покемона'''
        req = requests.get(url)
        self.json = req.json()
        self.name = self.json['name']
        self.power = self.json['power']
        self.type = self.json['type']['name']