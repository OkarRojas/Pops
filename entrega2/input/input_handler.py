import pygame
from confing import (
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ESCAPE
)


class InputHandler:
    """Gestiona la entrada del usuario y consume los eventos de pygame.

    Diseño:
    - Este componente es el único que debe llamar a `pygame.event.get()`.
    - Cuando detecta un evento QUIT, puede actualizar la ventana pasada
      (si se proporciona) o marcar `self.quit=True` si no se pasa ventana.

    Uso recomendado:
        input_handler.update(window)
        if input_handler.is_key_pressed(KEY_ESCAPE):
            window.close()
    """

    def __init__(self):
        # self.keys contendrá la secuencia devuelta por pygame.key.get_pressed()
        # o un diccionario vacío si se detecta cierre.
        self.keys = {}
        # Bandera interna de solicitud de quit si no se pasa window
        self.quit = False

    def update(self, window=None):
        """Actualizar el estado del input y consumir eventos.

        Si se proporciona `window`, se marcará `window.running = False` en
        caso de evento QUIT. Si no, `self.quit` se pondrá a True.
        """
        # Obtener el estado de las teclas (sequence)
        self.keys = pygame.key.get_pressed()

        # Consumir eventos y procesar QUIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if window is not None:
                    # Informar a window para que cierre
                    try:
                        # Preferimos llamar al método close() si existe
                        if hasattr(window, 'close'):
                            window.close()
                        else:
                            window.running = False
                    except Exception:
                        # Si no tiene atributo running/close, guardamos la bandera
                        self.quit = True
                else:
                    self.quit = True

    def is_key_pressed(self, key_name):
        """Consulta si una tecla lógica (p. ej. KEY_UP) está presionada.

        key_name: una de las constantes definidas en `confing.py`.
        """
        mapping = {
            KEY_UP:    pygame.K_w,
            KEY_DOWN:  pygame.K_s,
            KEY_LEFT:  pygame.K_a,
            KEY_RIGHT: pygame.K_d,
            KEY_ESCAPE:pygame.K_ESCAPE,
        }
        pygame_key = mapping.get(key_name)
        if pygame_key is None:
            return False

        # self.keys puede ser una secuencia (pygame.key.get_pressed()) o un dict
        try:
            return bool(self.keys[pygame_key])
        except Exception:
            if isinstance(self.keys, dict):
                return bool(self.keys.get(pygame_key, False))
            return False