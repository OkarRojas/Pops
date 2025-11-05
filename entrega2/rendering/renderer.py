import pygame

class renderer:
    def __init__(self, surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.default_font = pygame.font.SysFont(None, 24)

    def clear(self, color=(0, 0, 0)):
        """Limpia la superficie con el color especificado"""
        self.surface.fill(color)

    def draw_rect(self, x, y, width, height, color):
        """Dibuja un rectángulo en la superficie"""
        pygame.draw.rect(self.surface, color, (x, y, width, height))

    def draw_text(self, text, x, y, size=24, color=(255, 255, 255)):
        """Dibuja texto en la superficie"""
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        self.surface.blit(text_surface, (x, y))

    def present(self):
        """Actualiza la pantalla con todo lo dibujado"""
        pygame.display.flip()
