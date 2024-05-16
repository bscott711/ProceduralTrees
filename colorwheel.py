import pygame


class ColorWheel:

	def __init__(self, color: tuple, name: str = "name", pos: tuple = (0, 0)) -> None:
		self.colors = {"r": color[0], "g": color[1], "b": color[2]}
		self.name = name
		self.rect = pygame.Rect(pos[0], pos[1], 295, 90)
		self.channel_rects = {"r": pygame.Rect(19, 19, 257, 13), "g": pygame.Rect(19, 39, 257, 13), "b": pygame.Rect(19, 59, 257, 13)}
		self.surface = pygame.Surface(self.rect.size)
		self.generate_surface()
	

	def color(self) -> tuple:
		return pygame.Color(self.colors["r"], self.colors["g"], self.colors["b"])


	def generate_surface(self):
		self.surface.fill(self.color())
		for rect in self.channel_rects: # White background behind color bars
			pygame.draw.rect(self.surface, (255, 255, 255), self.channel_rects[rect])

		for i in range(255):
			pygame.draw.line(self.surface, (i, self.colors["g"], self.colors["b"]), (i + 20, 20), (i + 20, 30))
		for i in range(255):
			pygame.draw.line(self.surface, (self.colors["r"], i, self.colors["b"]), (i + 20, 40), (i + 20, 50))
		for i in range(255):
			pygame.draw.line(self.surface, (self.colors["r"], self.colors["g"], i), (i + 20, 60), (i + 20, 70))
		
		pygame.draw.rect(self.surface, (255, 255, 255), (self.colors["r"] + 19, 18, 4, 15))
		pygame.draw.rect(self.surface, (255, 255, 255), (self.colors["g"] + 19, 38, 4, 15))
		pygame.draw.rect(self.surface, (255, 255, 255), (self.colors["b"] + 19, 58, 4, 15))


	def update(self, mouse_x: int, mouse_y: int):
		for rect in self.channel_rects:
			if self.channel_rects[rect].collidepoint(mouse_x, mouse_y):
				self.colors[rect] = mouse_x - 20
				break
		self.generate_surface()


	def update_scroll(self, mouse_x: int, mouse_y: int, increment: int):
		for rect in self.channel_rects:
			if self.channel_rects[rect].collidepoint(mouse_x, mouse_y):
				self.colors[rect] = max(0, min(255, self.colors[rect] + increment))
				break
		self.generate_surface()

