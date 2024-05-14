import pygame
import random


green0 = (100, 140, 50)
green1 = (90, 130, 40)
green2 = (80, 120, 30)


def draw_leaf(surface, color, x, y):
	pygame.draw.rect(surface, color, (x, y, 12, 12))
	pygame.draw.rect(surface, color, (x + 4, y + 4, 12, 12))

def Leaf(age) -> pygame.Surface:
	width, height = 64, 64
	surface = pygame.Surface((width, height), pygame.SRCALPHA)

	for i in range(0, int(age / 600) + 1):
		j = i * 30
		draw_leaf(surface, green2, random.randint(j, width - j), random.randint(j, height - j))
	for i in range(0, int(age / 400) + 1):
		j = i * 15
		draw_leaf(surface, green1, random.randint(j, width - j), random.randint(j, height - j))
	for i in range(0, int(age / 200) + 1):
		j = i * 10
		draw_leaf(surface, green0, random.randint(j, width - j), random.randint(j, height - j))

	return surface

