# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from entrega2.config import BLACK, WHITE, KEY_ESCAPE

class GameEngine(object):
    def __init__(self, window_manager, renderer, input_handler, clock, scene=None):
        self.window = window_manager
        self.renderer = renderer
        self.input = input_handler
        self.clock = clock
        self.scene = scene or {"bricks": [], "texts": [], "entities": []}
        self.running = True
        self.on_start = None
        self.on_shutdown = None

    def run(self):
        if callable(self.on_start):
            self.on_start()
        while self.window.is_running() and self.running:
            dt = self.clock.tick()
            self.process_events()
            # If the window was closed during event processing, stop before
            # attempting update/render to avoid drawing on a quit Surface.
            if not self.window.is_running() or not self.running:
                break
            self.update(dt)
            self.render()
        if callable(self.on_shutdown):
            self.on_shutdown()
        self.window.close()

    def process_events(self):
        # Delegar a InputHandler el consumo de eventos; pasar la ventana
        self.input.update(self.window)
        if self.input.is_key_pressed(KEY_ESCAPE):
            self.running = False

    def update(self, delta_time):
        for e in self.scene.get("entities", []):
            upd = getattr(e, "update", None)
            if callable(upd):
                upd(delta_time, self.input)

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
