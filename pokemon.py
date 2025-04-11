# pokemon.py
import os
import pygame
import math
import random
import requests
import io
from urllib.request import urlopen
from constants import *
from move import Move
from ui import display_message
import time

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, level, x, y):
        '''Установка характеристик покемона'''
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.level = level
        self.x = x
        self.y = y
        self.num_potions = 3
        self.size = 150  # Установка размера до загрузки спрайтов

        # Загрузка данных с API
        self.json = self.load_pokemon_data()
        
        # Инициализация характеристик
        self.init_stats()
        self.init_types()
        self.set_moves()

        # Система анимации
        self.sprites = []
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.last_update = pygame.time.get_ticks()
        self.load_sprites()
        self.set_fallback_sprite()

        # Анимация исцеления
        self.heal_sprites = []
        self.current_heal_sprite = 0
        self.heal_animation_speed = 0.3
        self.healing_animation = False
        self.last_heal_update = 0
        self.load_heal_sprites()
        self.create_heal_fallback()

        # Флаги состояний
        self.is_attacking = False
        self.attack_start_time = 0
        self.attack_duration = 1000  # 1 секунда для атаки
        self.message = None
        self.message_start_time = 0
        self.message_duration = 1000  # 1 секунда для сообщений

    def load_pokemon_data(self):
        '''Загрузка данных покемона с PokeAPI'''
        try:
            req = requests.get(f'{BASE_URL}/pokemon/{self.name.lower()}')
            return req.json()
        except Exception as e:
            print(f"Error loading data for {self.name}: {e}")
            return {}

    def init_stats(self):
        '''Инициализация базовых характеристик'''
        base_stats = {
            'hp': 10,
            'attack': 5,
            'defense': 5,
            'speed': 5
        }

        if 'stats' in self.json:
            for stat in self.json['stats']:
                name = stat['stat']['name']
                base_stats[name] = stat['base_stat']

        self.max_hp = base_stats['hp'] + self.level
        self.current_hp = self.max_hp
        self.attack = base_stats['attack']
        self.defense = base_stats['defense']
        self.speed = base_stats['speed']

    def init_types(self):
        '''Инициализация типов покемона'''
        self.types = []
        if 'types' in self.json:
            for t in self.json['types']:
                self.types.append(t['type']['name'])

    def load_sprites(self):
        """Загрузка анимационных спрайтов"""
        sprite_folder = f"sprites/{self.name}"
        self.sprites = []
        
        try:
            # Проверка существования папки
            if not os.path.exists(sprite_folder):
                raise FileNotFoundError

            for i in range(1, 5):
                sprite_path = os.path.join(sprite_folder, f"{i}.png")
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprite = self.scale_sprite(sprite)
                    self.sprites.append(sprite)
        except Exception as e:
            print(f"Sprite loading error: {e}")

    def set_fallback_sprite(self):
        """Установка резервного спрайта"""
        if not self.sprites:
            try:
                # Попытка загрузки из API
                if 'sprites' in self.json:
                    sprite_url = self.json['sprites']['front_default']
                    image = urlopen(sprite_url).read()
                    image_file = io.BytesIO(image)
                    sprite = pygame.image.load(image_file).convert_alpha()
                    self.sprites = [self.scale_sprite(sprite)]
            except Exception as e:
                # Создание пустого спрайта
                print(f"Fallback sprite creation: {e}")
                self.sprites = [pygame.Surface((self.size, self.size), pygame.SRCALPHA)]

        self.image = self.sprites[0]

    def scale_sprite(self, sprite):
        """Масштабирование спрайта"""
        scale = self.size / max(sprite.get_size())
        return pygame.transform.smoothscale(
            sprite,
            (
                int(sprite.get_width() * scale),
                int(sprite.get_height() * scale)
            )
        )

    def load_heal_sprites(self):
        """Загрузка спрайтов исцеления"""
        self.heal_sprites = []
        try:
            for i in range(1, 8):
                path = f"sprites/heal/{i}.png"
                if os.path.exists(path):
                    sprite = pygame.image.load(path).convert_alpha()
                    self.heal_sprites.append(self.scale_sprite(sprite))
        except Exception as e:
            print(f"Heal sprite error: {e}")

    def create_heal_fallback(self):
        """Создание резервной анимации исцеления"""
        if not self.heal_sprites:
            size = int(self.size * 0.8)
            for alpha in range(50, 251, 50):
                surf = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(surf, (0, 255, 0, alpha), 
                                (size//2, size//2), size//3)
                self.heal_sprites.append(surf)

    def update_animation(self):
        """Обновление анимаций"""
        now = pygame.time.get_ticks()
        
        if self.healing_animation:
            if now - self.last_heal_update > self.heal_animation_speed * 1000:
                self.last_heal_update = now
                self.current_heal_sprite += 1
                if self.current_heal_sprite >= len(self.heal_sprites):
                    self.healing_animation = False
                    self.current_heal_sprite = 0
        else:
            if now - self.last_update > self.animation_speed * 1000:
                self.last_update = now
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
                self.image = self.sprites[self.current_sprite]

    def draw(self, game, alpha=255):
        """Отрисовка покемона"""
        self.update_animation()
        
        # Основной спрайт
        img = self.image.copy()
        img.fill((255,255,255,alpha), special_flags=pygame.BLEND_RGBA_MULT)
        game.blit(img, (self.x, self.y))
        
        # Анимация исцеления
        if self.healing_animation and self.heal_sprites:
            try:
                heal_img = self.heal_sprites[self.current_heal_sprite]
                pos = (
                    self.x + (self.image.get_width() - heal_img.get_width()) // 2,
                    self.y + (self.image.get_height() - heal_img.get_height()) // 2
                )
                game.blit(heal_img, pos)
            except (IndexError, pygame.error):
                self.healing_animation = False

    def perform_attack(self, other, move, game):
        """Выполнение атаки"""
        display_message(f'{self.name} использует {move.name}!', game)
        
        # Расчет урона
        base_damage = (2 * self.level + 10) / 250
        damage = base_damage * self.attack / other.defense * move.power
        if move.type in self.types:
            damage *= 1.5
        if random.random() <= 0.0625:  # 6.25% шанс крита
            damage *= 1.5
        final_damage = max(1, int(damage))
        
        other.take_damage(final_damage)
        display_message(f"Нанесено {final_damage} урона!", game)

    def take_damage(self, damage):
        """Получение урона"""
        self.current_hp = max(0, self.current_hp - int(damage))

    def use_potion(self):
        """Использование зелья"""
        if self.num_potions > 0:
            self.current_hp = min(self.max_hp, self.current_hp + 30)
            self.num_potions -= 1
            self.start_heal_animation()

    def start_heal_animation(self):
        """Запуск анимации исцеления"""
        self.healing_animation = True
        self.current_heal_sprite = 0
        self.last_heal_update = pygame.time.get_ticks()

    def set_moves(self):
        """Инициализация атак"""
        self.moves = []
        if 'moves' not in self.json:
            return
            
        # Фильтрация атак
        valid_moves = []
        for move_data in self.json['moves']:
            for version in move_data['version_group_details']:
                if (version['version_group']['name'] == 'red-blue' and
                    version['move_learn_method']['name'] == 'level-up' and
                    version['level_learned_at'] <= self.level):
                    try:
                        move = Move(move_data['move']['url'])
                        if move.power:
                            valid_moves.append(move)
                    except Exception as e:
                        print(f"Error loading move: {e}")
        
        # Выбор 4 случайных атак
        self.moves = random.sample(valid_moves, min(4, len(valid_moves)))

    def draw_hp(self, game):
        """Отрисовка шкалы здоровья"""
        bar_width = 200
        bar_height = 20
        pos = (self.hp_x, self.hp_y)
        
        # Фон
        pygame.draw.rect(game, RED, (pos[0], pos[1], bar_width, bar_height))
        
        # Текущее HP
        hp_width = (self.current_hp / self.max_hp) * bar_width
        pygame.draw.rect(game, GREEN, (pos[0], pos[1], hp_width, bar_height))
        
        # Текст
        font = pygame.font.Font(None, 24)
        text = font.render(f"HP: {self.current_hp}/{self.max_hp}", True, BLACK)
        game.blit(text, (pos[0], pos[1] + bar_height + 5))

    def get_rect(self):
        """Получение хитбокса"""
        if not hasattr(self, 'image') or self.image is None:
            return pygame.Rect(self.x, self.y, self.size, self.size)
        return self.image.get_rect(topleft=(self.x, self.y))