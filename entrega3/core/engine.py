from __future__ import unicode_literals
from entrega2.config import BLACK, WHITE, KEY_ESCAPE

from entrega3.integration.data_dictionary import DataDictionary
from entrega3.logic.game_logic import GameLogic 
from entrega2.integration.dnm_loader import load_scene_from_ast_file
from entrega2.integration.dnm_loader import ast_to_scene

class GameEngine(object):
    def __init__(self, window_manager, renderer, input_handler, clock, scene=None, ast=None, dnm_path=None):
        self.window = window_manager
        self.renderer = renderer
        self.input = input_handler
        self.clock = clock
        self.scene = scene or {"bricks": [], "texts": [], "entities": []}
        self.running = True
        self.on_start = None
        self.on_shutdown = None

        self.game_logic = None
        if ast is not None or dnm_path is not None:
            if ast is None and dnm_path:
                ast = load_scene_from_ast_file(dnm_path) 
                self.scene = ast_to_scene(ast)

            self.data_dict = DataDictionary(ast)
            self.game_logic = GameLogic(self.data_dict, self.scene["entities"])

    def run(self):
        if callable(self.on_start):
            self.on_start()

        while self.window.is_running() and self.running:
            dt = self.clock.tick(60) / 1000.0 

            self.process_events()
            if not self.window.is_running() or not self.running:
                break

            if self.game_logic:
                self.game_logic.update(dt, self.input, self.scene)
            else:
                for e in self.scene.get("entities", []):
                    upd = getattr(e, "update", None)
                    if callable(upd):
                        upd(dt, self.input)

            self.render()

        if callable(self.on_shutdown):
            self.on_shutdown()
        self.window.close()

    def process_events(self):
        self.input.update(self.window)
        if self.input.is_key_pressed(KEY_ESCAPE):
            self.running = False

    def render(self):
        self.renderer.clear(BLACK)
        for b in self.scene.get("bricks", []):
            self.renderer.draw_rect(b["x"], b["y"], b["w"], b["h"], b["color"])
        for e in self.scene.get("entities", []):
            dr = getattr(e, "draw", None)
            if callable(dr):
                dr(self.renderer)
        for t in self.scene.get("texts", []):
            self.renderer.draw_text(t["text"], t["x"], t["y"], t.get("size", 16), t.get("color", WHITE))
        self.renderer.present()