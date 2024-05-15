import pygame
import palette
from tree import Tree


pygame.init()
window = pygame.display.set_mode((1280, 720))


tree = Tree(palette.load_palette("cherry"), 50)


while True:
	tree.grow()

	window.fill((130, 170, 70))
	tree.draw(window, (635, 200))

	# Side panel
	pygame.draw.rect(window, (120, 125, 130), (0, 0, 350, 720))
	# Button
	pygame.draw.rect(window, (50, 55, 60), (15, 15, 320, 40))
	
	pygame.display.flip()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			tree.change_color(palette.load_palette("autumn"))


