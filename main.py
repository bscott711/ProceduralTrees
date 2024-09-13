import pygame, cv2, numpy as np
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

images = []
image = pygame.Surface(tree.surface.size, pygame.SRCALPHA)
image.fill((130, 170, 70, 255))
video_fps = 60


while True:
	if tree.grow():
		new_image = image.copy()
		new_image.blit(tree.surface, (0, 0))
		images.append(pygame.surfarray.array3d(new_image))
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
				images = []
				print("generating new tree")
			elif save_button_rect.collidepoint(event.pos):
				new_image = image.copy()
				new_image.blit(tree.surface, (0, 0))
				pygame.image.save(new_image,'tree.png')
				print("Image saved as tree.png")

				fourcc = cv2.VideoWriter_fourcc(*'mp4v')
				video_writer = cv2.VideoWriter("video.mp4", fourcc, video_fps, tree.surface.size)

				# Iterate through each surface and write it to the video
				for frame in images:
					frame = np.transpose(frame, (1, 0, 2))  # Pygame surface is transposed
					frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
					video_writer.write(frame)

				video_writer.release()
				print(f"Video saved as video.mp4")


