import pygame 

class windows_manager:
    def __init__(self, width, height,title):
        
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.running = True

    def get_surface(self):
         return self.screen 
    
    def is_running(self):
        # Procesar eventos de pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        return self.running

    def close(self):
        self.running = False
        pygame.quit()
        