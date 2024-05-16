import pygame


class Button:

	def __init__(self, text: str, size: list, pos: list):
		self.text = text
		self.size = size
		self.pos = pos
		
		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.center = (self.size[0] / 2, self.size[1] / 2)
		self.surface = pygame.Surface(size, pygame.SRCALPHA)
		
		self.hovered = False
		self.focused = False
		self.regenerate()
		

	def set_text(self):
		font = pygame.font.Font(None, 26)
		text_surface = font.render(self.text, True, (240, 240, 240))
		text_rect = text_surface.get_rect()
		text_rect.center = self.center
		self.surface.blit(text_surface, text_rect)

	def regenerate(self):
		if (self.hovered):
			pygame.draw.rect(self.surface, (120, 90, 150), (0, 0, self.size[0], self.size[1]), border_radius=8)
		else:
			pygame.draw.rect(self.surface, (90, 60, 80), (0, 0, self.size[0], self.size[1]), border_radius=8)
		pygame.draw.rect(self.surface, (100, 90, 90), (0, 0, self.size[0], self.size[1]), 4, 8)
		self.set_text()

	def draw_to(self, window: pygame.Surface):
		window.blit(self.surface, self.pos)

	def clicked(self) -> str:
		return self.text