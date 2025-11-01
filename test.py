import pygame
from confing import *
from entrega2.rendering.windows_manager import windows_manager
from entrega2.rendering.renderer import renderer

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
renderer = renderer(surface)

# PASO 4: Game Loop Simple
print("4. Iniciando game loop...")
frame_count = 0
max_frames = 300  # Ejecutar 300 frames (5 segundos a 60 FPS)

while window.is_running() and frame_count < max_frames:
    frame_count += 1
    
    # Dibujar
    renderer.clear(BLACK)                                   # Limpiar
    renderer.draw_rect(100, 100, 40, 40, RED)              # Rectángulo rojo
    renderer.draw_rect(300, 200, 50, 50, BLUE)             # Rectángulo azul
    renderer.draw_text("Test de Pygame", 10, 10, 20, WHITE)  # Texto
    renderer.draw_text(f"Frame: {frame_count}", 10, 40, 20, GREEN)
    renderer.present()                                      # Mostrar

# PASO 5: Cerrar
print("5. Cerrando...")
window.close()
print("✓ Test completado!")
