"""Window manager sencillo para crear la ventana y exponer la surface.

Este módulo no debe consumir eventos: `InputHandler` es el componente
responsable de llamar a `pygame.event.get()` y notificar cierres.
"""

import pygame


class windows_manager:
    """Gestor de ventana mínimo.

    Aclaro que la clase mantiene el nombre `windows_manager` en minúsculas
    para mantener compatibilidad con el resto del código del proyecto.
    """

    def __init__(self, width, height, title):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title

        # Crear la pantalla y configurar título
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        # Bandera que indica si la ventana debe seguir abierta
        self.running = True

    def get_surface(self):
        """Devuelve el surface principal (pygame.Surface)."""
        return self.screen

    def is_running(self):
        """Indica si la ventana está activa.

        No consume eventos; InputHandler.update(window) debe actualizar
        `self.running` cuando reciba un QUIT.
        """
        return self.running

    def close(self):
        """Cerrar la ventana y finalizar pygame limpiamente."""
        self.running = False
        pygame.quit()

        