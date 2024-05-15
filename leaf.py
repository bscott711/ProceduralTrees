import pygame
import random
import constants as cts


def draw_leaf(surface, color, x, y):
	pygame.draw.rect(surface, color, (x, y, 12, 12))
	pygame.draw.rect(surface, color, (x + 4, y + 4, 12, 12))

def random_leaves() -> pygame.Surface:
	width, height = 64, 64
	surface = pygame.Surface((width, height), pygame.SRCALPHA)

	for i in range(0, 1):
		j = i * 30
		draw_leaf(surface, cts.green2, random.randint(j, width - j), random.randint(j, height - j))
	for i in range(0, 2):
		j = i * 15
		draw_leaf(surface, cts.green1, random.randint(j, width - j), random.randint(j, height - j))
	for i in range(0, 3):
		j = i * 10
		draw_leaf(surface, cts.green0, random.randint(j, width - j), random.randint(j, height - j))

	return surface

