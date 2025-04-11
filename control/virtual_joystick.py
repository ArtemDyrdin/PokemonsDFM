from pygame.locals import *


# Эмуляция джойстиков с клавиатуры
KEYBOARD_JOYSTICK_MAPPING = {
    # Игрок 1
    K_w: ('P1B0', 1),  # Вверх
    K_s: ('P1B1', 1),  # Вниз
    K_a: ('P1B2', 1),  # Влево
    K_d: ('P1B3', 1),  # Вправо
    K_f: ('P1B4', 1),  # Огонь
    
    # Игрок 2
    K_UP: ('P2B0', 1),    # Вверх
    K_DOWN: ('P2B1', 1),  # Вниз
    K_LEFT: ('P2B2', 1),  # Влево
    K_RIGHT: ('P2B3', 1), # Вправо
    K_RETURN: ('P2B4', 1) # Огонь
}

class VirtualJoystick:
    def __init__(self):
        self.buffer = []
    
    def write(self, data):
        """Эмулирует получение данных от Arduino"""
        self.buffer.append(data)
    
    def readline(self):
        if self.buffer:
            return self.buffer.pop(0).encode('utf-8')
        return b''
    
    @property
    def in_waiting(self):
        return len(self.buffer)
    