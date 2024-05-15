import pygame
import random
import constants as cts



def random_pos():
	return (random.randint(0, cts.leaf_surface_width), random.randint(0, cts.leaf_surface_height))

def draw_leaf(surface, color: str, pos: tuple):
	pygame.draw.rect(surface, color, (pos[0], pos[1], 12, 12))
	pygame.draw.rect(surface, color, (pos[0] + 4, pos[1] + 4, 12, 12))
	

class Leaves:

	def __init__(self, palette: dict) -> None:
		self.palette = palette
		self.size = (cts.leaf_surface_width, cts.leaf_surface_height)
		self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
		self.leaves = [[random_pos() for _ in range(num_leaves)] for num_leaves in cts.leaves_density]
		self.generate_surface()

	def generate_surface(self):
		for leaf_pos in self.leaves[0]:
			draw_leaf(self.surface, self.palette["leaves0"], leaf_pos)
		for leaf_pos in self.leaves[1]:
			draw_leaf(self.surface, self.palette["leaves1"], leaf_pos)
		for leaf_pos in self.leaves[2]:
			draw_leaf(self.surface, self.palette["leaves2"], leaf_pos)

