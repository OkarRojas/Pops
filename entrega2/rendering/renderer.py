import pygame


class Renderer:
	"""Renderer sencillo que dibuja sobre una superficie pygame.

	Provee helpers mínimos: clear, draw_rect, draw_text y present.
	Mantiene una caché de fuentes por tamaño para evitar recrearlas cada frame.
	"""

	def __init__(self, surface):
		self.surface = surface
		self._font_cache = {}

	def clear(self, color):
		"""Limpia la superficie completa con el color indicado."""
		self.surface.fill(color)

	def draw_rect(self, x, y, width, height, color):
		"""Dibuja un rectángulo relleno en la surface."""
		pygame.draw.rect(self.surface, color, (x, y, width, height))

	def draw_text(self, text, x, y, font_size=20, color=(0, 0, 0)):
		"""Dibuja texto en la surface en la posición indicada.

		`text` se convierte a str por seguridad. `font_size` controla la talla.
		"""
		font = self._font_cache.get(font_size)
		if font is None:
			font = pygame.font.SysFont(None, font_size)
			self._font_cache[font_size] = font
		text_surf = font.render(str(text), True, color)
		self.surface.blit(text_surf, (x, y))

	def present(self):
		"""Volcar el buffer a la pantalla (flip)."""
		pygame.display.flip()

