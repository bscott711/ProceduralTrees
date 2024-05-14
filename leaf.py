import pygame
import random

def pixellate(surface: pygame.Surface):
	width, height = surface.get_size()
	small = pygame.transform.scale(surface, (width // 4, height // 4))
	return pygame.transform.scale(small, (width, height))

# green0 = (96, 173, 87)
# green1 = (57, 139, 70)
# green2 = (0, 98, 56)
# green0 = (190, 180, 59)
# green1 = (140, 131, 15)
# green2 = (116, 118, 17)
green0 = (100, 140, 50)
green1 = (90, 130, 40)
green2 = (80, 120, 30)



def draw_circles(surface, size, x, y):
	pygame.draw.circle(surface, (green0), (x, y - 2), size) # Top (bright)
	pygame.draw.circle(surface, (green2), (x, y + 2), size) # Bottom (dark)
	pygame.draw.circle(surface, (green1), (x, y), size - 2) # Center (medium)



def clump() -> pygame.Surface:
	surface = pygame.Surface((100, 100), pygame.SRCALPHA)
	surface.fill((0, 0, 0, 0.2))

	for i in range(random.randint(3, 10), 1, -1):
		draw_circles(surface, random.randint(i * 3, i * 4), random.randint(25 + i, 55 - i), random.randint(25 + i, 55 - i))
	for i in range(random.randint(3, 20), 1, -1):
		x, y = random.randint(25, 55), random.randint(25, 55)
		pygame.draw.line(surface, green2, (x, y), (x, y + random.randint(10, 30)), 4)

	return surface

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




# pygame.init()

# window = pygame.display.set_mode((900, 700))
# window.fill((61, 101, 93))
# window.blit(clump2(200), (300, 200))
# pygame.display.flip()

# while True:


# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			quit()
# 		elif (event.type == pygame.MOUSEBUTTONDOWN):
# 			window.fill((61, 101, 93))
# 			window.blit(clump2(200), (300, 200))
# 			pygame.display.flip()
