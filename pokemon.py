# pokemon.py
import os
import pygame
import math
import random
from constants import *
from move import Move
from ui import display_message
import time

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, level, x, y, data):
        '''Установка имени, уровня, позиции на экране и количество зелий покемона'''
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.level = level
        self.x = x
        self.y = y
        self.num_potions = 3
        self.data = data[name]

        # Атрибуты для анимации
        self.sprites = []  # Список для хранения кадров анимации
        self.current_sprite = 0  # Текущий кадр
        self.animation_speed = 0.2  # Скорость анимации
        self.last_update = pygame.time.get_ticks()  # Время последнего обновления
        
        self.current_hp = self.data['HP'] + self.level
        self.max_hp = self.data['HP'] + self.level
        self.attack = self.data['Attack']
        self.defense = self.data['Defense']
        self.speed = self.data['Speed']

        # сохрание типов покемона
        self.types = self.data['Types']

        self.size = 150
        self.load_sprites()

    def load_sprites(self):
        """Загружает 4 спрайта анимации из локальной папки"""
        sprite_folder = f"sprites/{self.name}"
        
        # Загружаем 4 спрайта (1.png, 2.png, 3.png, 4.png)
        for i in range(1, 5):
            sprite_path = os.path.join(sprite_folder, f"{i}.png")
            try:
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    # Масштабируем спрайт
                    scale = self.size / sprite.get_width()
                    new_width = int(sprite.get_width() * scale)
                    new_height = int(sprite.get_height() * scale)
                    sprite = pygame.transform.scale(sprite, (new_width, new_height))
                    self.sprites.append(sprite)
            except Exception as e:
                print(f"Error loading sprite {sprite_path}: {e}")

    def update_animation(self):
        '''Обновляет текущий кадр анимации'''
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:  # Преобразуем секунды в миллисекунды
            self.last_update = now
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]

    def draw(self, game, alpha=255):
        '''Отрисовывает покемона на экране с анимацией'''
        self.update_animation()  # Обновляем анимацию
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    def perform_attack(self, other, move, game):
        '''Выполняет атаку на другого покемона'''
        display_message(f'{self.name} used {move.name}', game)
        time.sleep(2)
        damage = (2 * self.level + 10) / 250 * self.attack / other.defense * move.power
        if move.type in self.types:
            damage *= 1.5
        random_num = random.randint(1, 10000)
        if random_num <= 625:
            damage *= 1.5
        damage = math.floor(damage)
        other.take_damage(damage)

    def take_damage(self, damage):
        '''Уменьшает здоровье покемона на указанное значение'''
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def use_potion(self):
        '''Использует зелье для восстановления здоровья'''
        if self.num_potions > 0:
            self.current_hp += 30
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            self.num_potions -= 1

    def set_moves(self):
        '''Загружает атаки покемона'''
        self.moves = []
        attaks = self.data['Attacks']
        for attak in attaks:
            move = Move(attak)
            if move.power is not None:
                self.moves.append(move)
        if len(self.moves) > 4:
            self.moves = random.sample(self.moves, 4)

    def draw_hp(self, game):
        '''Отрисовывает полоску здоровья покемона'''
        bar_scale = 200 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, RED, bar)
        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, GREEN, bar)
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.current_hp} / {self.max_hp}', True, BLACK)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        game.blit(text, text_rect)

    def get_rect(self):
        '''Получить параметры прямоугольника спрайта покемона'''
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())