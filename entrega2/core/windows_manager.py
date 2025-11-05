import pygame


class WindowManager:
	def __init__(self, width: int, height: int, title: str):
		self._surface = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		self._running = True

	def get_surface(self):
		return self._surface

	def is_running(self) -> bool:
		return self._running

	def close(self) -> None:
		self._running = False
