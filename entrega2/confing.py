"""Constantes de configuración del proyecto.

No cambiar el nombre del archivo (`confing.py`) porque muchos módulos
import usando ese nombre. Contiene valores sencillos para ventanas,
colores y teclas lógicas.
"""

WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE = 800, 600, "Pygame Window Test"

# Game / rendering
FPS = 60

# Movement
MOVE_SPEED = 5

# Key names used by InputHandler (lógicos, mapeados a teclas físicas)
KEY_UP = 'UP'
KEY_DOWN = 'DOWN'
KEY_LEFT = 'LEFT'
KEY_RIGHT = 'RIGHT'
KEY_ESCAPE = 'ESCAPE'

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
