import pygame
from palette import load_palette
from tree import Tree

def button(w, h, text):
	button_rect = pygame.Surface((w, h), pygame.SRCALPHA)
	pygame.draw.rect(button_rect, (255, 255, 255), (0, 0, w, h), 0, 8)
	pygame.draw.rect(button_rect, (55, 55, 55), (0, 0, w, h), 4, 8)

	font = pygame.font.Font('freesansbold.ttf', 16)
	text = font.render(text, True, (55, 55, 55))
	textRect = text.get_rect()
	textRect.center = (w // 2, h // 2 + 2)
	button_rect.blit(text, textRect)

	return button_rect


pygame.init()
window = pygame.display.set_mode((400, 600))
palette = load_palette("green")
tree = Tree(palette, 50)
new_tree_button_surf = button(100, 50, "New Tree")
new_tree_button_rect = pygame.Rect(20, 20, 100, 50)
save_button_surf = button(100, 50, "Save")
save_button_rect = pygame.Rect(140, 20, 100, 50)


while True:
	tree.grow()
	window.fill((130, 170, 70))
	tree.draw(window, (0, 0))
	window.blit(new_tree_button_surf, new_tree_button_rect)
	window.blit(save_button_surf, save_button_rect)
	pygame.display.flip()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			if new_tree_button_rect.collidepoint(event.pos):
				tree = Tree(palette, 50)
				print("generating new tree")
			elif save_button_rect.collidepoint(event.pos):
				image = pygame.Surface(tree.surface.size, pygame.SRCALPHA)
				image.fill((130, 170, 70, 255))
				image.blit(tree.surface, (0, 0))
				pygame.image.save(image,'tree.png')
				print("saved", tree.surface.size)


