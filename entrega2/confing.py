"""Compatibility wrapper: expose the canonical `config.py` names under
the historical module name `confing` (many files import `entrega2.confing`).

Keep this file minimal so future edits stay in `config.py` only.
"""

from .config import *

__all__ = [
	'WINDOW_WIDTH', 'WINDOW_HEIGHT', 'WINDOW_TITLE',
	'FPS', 'MOVE_SPEED',
	'KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT', 'KEY_ESCAPE',
	'BLACK', 'WHITE', 'RED', 'GREEN', 'BLUE'
]
