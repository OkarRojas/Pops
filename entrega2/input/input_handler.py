import pygame
from confing import (
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ESCAPE
)

class InputHandler:
    def __init__(self):
        self.keys = {}

    def update(self):
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keys = {}  # fuerza cierre

    def is_key_pressed(self, key_name: str) -> bool:
        mapping = {
            KEY_UP:    pygame.K_UP,
            KEY_DOWN:  pygame.K_DOWN,
            KEY_LEFT:  pygame.K_LEFT,
            KEY_RIGHT: pygame.K_RIGHT,
            KEY_ESCAPE:pygame.K_ESCAPE,
        }
        pygame_key = mapping.get(key_name)
        if not pygame_key:
            return False

        # self.keys can be a sequence (pygame.key.get_pressed()) or a dict (e.g. {})
        try:
            # Sequence access (most common)
            return bool(self.keys[pygame_key])
        except Exception:
            # Fallback to dict-like access
            if isinstance(self.keys, dict):
                return bool(self.keys.get(pygame_key, False))
            return False