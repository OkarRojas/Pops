import pygame


class WindowManager:
	def __init__(self, width, height, title):
		self._surface = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		self._running = True

	def get_surface(self):
		return self._surface

	def is_running(self):
		return self._running

	def close(self):
		self._running = False
