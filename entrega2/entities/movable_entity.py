import pygame
# Use the shared `confing.py` (intentionally named) so key names and
# movement constants are the same the InputHandler expects.
from entrega2.confing import MOVE_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT


class MovableEntity:
    """Entidad simple que puede moverse y dibujarse.

    Atributos:
        rect: pygame.Rect que representa la posición y tamaño.
        color: tupla RGB del color de la entidad.
    """

    def __init__(self, x, y, color=(255, 100, 100)):
        self.rect = pygame.Rect(x, y, 50, 30)
        self.color = color

    def update(self, delta_time, input_handler):
        """Actualizar posición según entradas del InputHandler.

        Firma compatible con el motor: update(delta_time, input_handler)
        """
        # Usa las constantes definidas en config para consultar teclas
        if input_handler.is_key_pressed(KEY_UP):
            self.rect.y -= MOVE_SPEED
        if input_handler.is_key_pressed(KEY_DOWN):
            self.rect.y += MOVE_SPEED
        if input_handler.is_key_pressed(KEY_LEFT):
            self.rect.x -= MOVE_SPEED
        if input_handler.is_key_pressed(KEY_RIGHT):
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
