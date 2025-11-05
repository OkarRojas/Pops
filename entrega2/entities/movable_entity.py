import pygame
from confing import MOVE_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT


class MovableEntity:
    """Entidad simple que puede moverse y dibujarse.

    Atributos:
        rect: pygame.Rect que representa la posición y tamaño.
        color: tupla RGB del color de la entidad.
    """

    def __init__(self, x, y, color=(255, 100, 100)):
        self.rect = pygame.Rect(x, y, 50, 30)
        self.color = color

    def update(self, input_handler):
        """Actualizar posición según entradas del InputHandler."""
        if input_handler.is_key_pressed('UP'):
            self.rect.y -= MOVE_SPEED
        if input_handler.is_key_pressed('DOWN'):
            self.rect.y += MOVE_SPEED
        if input_handler.is_key_pressed('LEFT'):
            self.rect.x -= MOVE_SPEED
        if input_handler.is_key_pressed('RIGHT'):
            self.rect.x += MOVE_SPEED

        # límites pantalla (usar constantes de configuración)
        self.rect.x = max(0, min(self.rect.x, WINDOW_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, WINDOW_HEIGHT - self.rect.height))

    def draw(self, renderer):
        """Dibuja la entidad usando el renderer (draw_rect)."""
        renderer.draw_rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.color,
        )
