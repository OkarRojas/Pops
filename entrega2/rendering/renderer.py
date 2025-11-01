import pygame

class renderer:
    def __init__(self, surface):
        pygame.init()
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.x = 0
        self.y = 0
        self.color = (0, 0, 0)  # Default background color
        self.font = pygame.font.SysFont(None, 24)

    def clear_surface(self):
        self.surface.fill(self.color)

    def draw(self, x, y, width, height, color):
        self.clear_surface()
        pygame.draw.rect(self.surface, color, (x, y, width, height))
        self.screen.blit(self.surface, (self.x, self.y))

    def draw_text(self, text, font, color, position):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def present(self):
        pygame.display.flip()
