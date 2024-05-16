import json
import pygame
from button import Button
from colorwheel import ColorWheel

filename = "palettes.json"


class CustomEncoder(json.JSONEncoder): # Chatgpt code to make the json files easier to read
	def encode(self, obj):
		json_str = super().encode(obj)
		# Post-process to reduce list indentation
		json_str = json_str.replace('[\n            ', '[')
		json_str = json_str.replace('\n            ', ' ')
		json_str = json_str.replace('\n        ]', ']')
		return json_str


def load():
	with open(filename, "r") as file:
		palettes = json.load(file)
	
	# Nested for loop to get each color in each palette and convert the color to a tuple
	return {palette: {color: tuple(palettes[palette][color]) for color in palettes[palette]} for palette in palettes}


def load_palette(name: str):
	return load()[name]


def save_palette(name: str, colors: dict[str, tuple]):
	# Converts tuples to lists
	colors = {color: list(colors[color]) for color in colors}
	saved = load()
	saved[name] = colors
	json_data = json.dumps(saved, cls = CustomEncoder, indent = 4)
	with open(filename, "w") as file:
		file.write(json_data)


class PaletteEditor:

	def __init__(self, name: str) -> None:
		self.name = name
		self.palette = load_palette(name)
		self.preview_rects = {color: pygame.Rect(240, 70 + (count * 28), 26, 26) for count, color in enumerate(self.palette)}
		self.surface = pygame.Surface((335, 500))
		self.title_font = pygame.font.Font(None, 40)
		self.color_font = pygame.font.Font(None, 28)
		self.title = self.title_font.render("Palette: " + self.name, True, (255, 255, 255))
		self.editing = None
		self.save_button = Button("Save", [120, 50], [108, 430])
		self.generate_surface()

	def generate_surface(self):
		self.surface.fill((33, 30, 36))
		self.surface.blit(self.title, (25, 30)) # Title
		for count, color in enumerate(self.palette):
			text_surf = self.color_font.render("- " + color.capitalize() + ":", True, (255, 255, 255))
			self.surface.blit(text_surf, (40, 70 + (count * 28))) # Draws the name of the color
			pygame.draw.rect(self.surface, self.palette[color], self.preview_rects[color], 0, 7) # Draws a review of the color
		self.save_button.draw_to(self.surface)
				

	def update(self, mouse_x: int, mouse_y: int) -> bool:
		if self.editing != None:
			if self.editing.rect.collidepoint(mouse_x, mouse_y):
				self.editing.update(mouse_x - 30, mouse_y - self.editing.rect.top)
				self.palette[self.editing.name] = self.editing.color()
				self.generate_surface()
				self.surface.blit(self.editing.surface, self.editing.rect)
				return True
		if self.save_button.rect.collidepoint(mouse_x, mouse_y):
			save_palette("custom" + str(len(load()) - 3), self.palette)
			return False
		for count, color in enumerate(self.preview_rects):
			if self.preview_rects[color].collidepoint(mouse_x, mouse_y):
				self.generate_surface()
				self.editing = ColorWheel(self.palette[color], name = color, pos = (30, 98 + (count * 28)))
				self.editing.generate_surface()
				self.surface.blit(self.editing.surface, (30, 98 + (count * 28)))
				return False

		self.editing = None
		self.generate_surface()
		return False