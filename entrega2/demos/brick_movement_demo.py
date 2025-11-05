import pygame
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ENTREGA2_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if ENTREGA2_DIR not in sys.path:
    sys.path.insert(0, ENTREGA2_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from confing import BLUE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS, WHITE, RED
from rendering.windows_manager import windows_manager
from rendering.renderer import Renderer
from input.input_handler import InputHandler
from entities.movable_entity import MovableEntity

def main():
    window = windows_manager(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    renderer = Renderer(window.get_surface())

    input_handler = InputHandler()
    brick = MovableEntity(295, 225, RED)

    clock = pygame.time.Clock()
    while window.is_running():
        input_handler.update()
        if input_handler.is_key_pressed('ESCAPE'):
            window.close()

        brick.update(input_handler)

        renderer.clear(BLUE)
        brick.draw(renderer)
        renderer.draw_text(
            "Flechas = mover  |  ESC = salir",
            10, 10, 20, (255, 255, 255)
        )
        renderer.present()

        clock.tick(FPS)

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()