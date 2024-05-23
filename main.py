import pygame
from palette import load_palette
from tree import Tree


pygame.init()
window = pygame.display.set_mode((400, 600))
palette = load_palette("green")
tree = Tree(palette, 50)


while True:
	tree.grow()
	window.fill((130, 170, 70))
	tree.draw(window, (0, 0))
	pygame.display.flip()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			tree = Tree(palette, 50)

