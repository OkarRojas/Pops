"""Pequeña prueba de integración: crea una ventana, procesa input y dibuja
una entidad móvil usando los componentes del proyecto.

Este archivo se usa para comprobar que `windows_manager`, `Renderer`,
`InputHandler` y `MovableEntity` funcionan juntos.
"""

from confing import *
from rendering.windows_manager import windows_manager
from rendering.renderer import Renderer
from input.input_handler import InputHandler
from entities.movable_entity import MovableEntity
import pygame


# PASO 1: Crear ventana
print("1. Creando ventana...")
window = windows_manager(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

# PASO 2: Obtener Surface
print("2. Obteniendo Surface...")
surface = window.get_surface()
if surface is None:
    print("❌ ERROR: get_surface() retornó None")
    exit()
print(f"✓ Surface obtenido: {surface}")

# PASO 3: Crear Renderer
print("3. Creando Renderer...")
renderer = Renderer(surface)

# PASO 4: Game Loop Simple
print("4. Iniciando game loop...")

input_handler = InputHandler()
brick = MovableEntity(295, 225, RED)
clock = pygame.time.Clock()


while window.is_running():
    # InputHandler es el único que consume eventos: le pasamos la ventana
    input_handler.update(window)
    # Si al procesar eventos se solicitó cierre, salir del bucle antes de dibujar
    if not window.is_running():
        break
    if input_handler.is_key_pressed(KEY_ESCAPE):
        window.close()
        break

    # Actualizar entidad
    brick.update(input_handler)

    # Dibujar: limpiamos y pedimos a la entidad que se dibuje vía renderer
    renderer.clear(BLACK)
    brick.draw(renderer)
    # Texto de información
    renderer.draw_text("Test de Pygame", 10, 10, 20, WHITE)
    renderer.draw_text("Frame: holas", 10, 40, 20, GREEN)
    renderer.present()
    clock.tick(FPS)

# PASO 5: Cerrar
print("5. Cerrando...")
print("Test completado!")
