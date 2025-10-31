import pygame

class renderer:
    def __init__(self, width, height, x, y, color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def clear_surface(self):
        surface = pygame.Surface((self.width, self.height))
        surface.fill(self.color)
        return surface
    
    def draw(self, screen):
        surface = self.clear_surface()
        screen.blit(surface, (self.x, self.y))

    def draw_text(self, screen, text, font, color, position):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)

    def present(self):
        pygame.display.flip()
    def shutdown(self):
        pygame.quit()