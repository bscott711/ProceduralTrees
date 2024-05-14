import pygame
from tree import Tree


pygame.init()
window = pygame.display.set_mode((1080, 720))


tree0 = Tree()
tree1 = Tree()
tree2 = Tree()


while True:
	tree0.grow()
	tree1.grow()
	tree2.grow()

	window.fill((130, 170, 70))
	tree0.draw(window, (0, 200))
	tree1.draw(window, (360, 200))
	tree2.draw(window, (720, 200))
	
	pygame.display.flip()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			tree0 = Tree()
			tree1 = Tree()
			tree2 = Tree()



