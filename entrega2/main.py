# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from entrega2.config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS
from entrega2.core.clock import Clock
from entrega2.core.engine import GameEngine
from entrega2.integration.dnm_loader import load_scene_from_ast_file

# Implementados por Persona 1 y 3
from entrega2.core.window_manager import WindowManager
from entrega2.rendering.renderer import Renderer
from entrega2.input.input_handler import InputHandler

def main():
    try:
        scene = load_scene_from_ast_file("arboldnm.ast")
        w = scene.get("window", {}).get("width", WINDOW_WIDTH)
        h = scene.get("window", {}).get("height", WINDOW_HEIGHT)
        title = scene.get("window", {}).get("title", WINDOW_TITLE)
    except Exception:
        scene, w, h, title = {"bricks": [], "texts": [], "entities": []}, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

    window = WindowManager(w, h, title)
    renderer = Renderer(window.get_surface())
    input_handler = InputHandler()
    clock = Clock(FPS)
    engine = GameEngine(window, renderer, input_handler, clock, scene)
    engine.run()

if __name__ == "__main__":
    main()
