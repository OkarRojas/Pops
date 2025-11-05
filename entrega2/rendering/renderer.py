import pygame


class Renderer:
	"""Renderer sencillo que dibuja sobre una superficie pygame."""

	def __init__(self, surface):
		self.surface = surface
		self._font_cache = {}

	def clear(self, color):
		self.surface.fill(color)

	def draw_rect(self, x, y, width, height, color):
		pygame.draw.rect(self.surface, color, (x, y, width, height))

	def draw_text(self, text, x, y, font_size=20, color=(0, 0, 0)):
		font = self._font_cache.get(font_size)
		if font is None:
			font = pygame.font.SysFont(None, font_size)
			self._font_cache[font_size] = font
		text_surf = font.render(str(text), True, color)
		self.surface.blit(text_surf, (x, y))

	def present(self):
		pygame.display.flip()
