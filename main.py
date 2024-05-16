import pygame
import palette
from tree import Tree

pygame.init()
window = pygame.display.set_mode((1280, 720))


palette_editor = palette.PaletteEditor("custom0")
tree = Tree(palette_editor.palette, 50)
palette_editor.generate_surface()

while True:
	tree.grow()

	window.fill((130, 170, 70)) # Clears the screen
	tree.draw(window, (635, 200))
	window.blit(palette_editor.surface, (0, 0))
	pygame.display.flip()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			if event.button == 1:
				if palette_editor.update(event.pos[0], event.pos[1]):
					tree.change_color(palette_editor.palette)


