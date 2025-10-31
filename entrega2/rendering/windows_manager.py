import pygame 

class windows_manager:
    def __init__(self, width, height, x, y, color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def get_surface(self):
        surface = pygame.Surface((self.width, self.height))
        surface.fill(self.color)
        return surface
    
    def is_runing(self, event):
        if event.type == pygame.QUIT:
            return False
        return True
    
    def draw_window(self, screen):
        surface = self.gef_surface()
        screen.blit(surface, (self.x, self.y))

    def close_window(self):
        pygame.quit()
        