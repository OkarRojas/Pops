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
    
    def is_running(self, event):
        if event.type == pygame.QUIT:
            return self.running == False
        return True

    def close_window(self):
        pygame.quit()
        