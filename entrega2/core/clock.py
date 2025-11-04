# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

class Clock(object):
    def __init__(self, target_fps=60):
        self.target_fps = target_fps
        self._dt = 0.0
        self._last = time.time()

    def delta(self):
        return self._dt

    def tick(self):
        now = time.time()
        self._dt = now - self._last
        if self.target_fps:
            min_frame = 1.0 / float(self.target_fps)
            if self._dt < min_frame:
                time.sleep(min_frame - self._dt)
                now = time.time()
                self._dt = now - self._last
        self._last = now
        return self._dt
