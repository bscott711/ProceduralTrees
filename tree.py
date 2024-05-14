import pygame
import node as nd

Node = nd.Node


class Tree:

	def __init__(self) -> None:
		self.age = 0
		self.rect = pygame.Rect(0, 0, 360, 460)
		self.branches = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.leaves = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.root = Node(self.age, 26, 90)

	def grow(self):
		if (nd.count(self.root) < 50):
			self.age += 1
			grow_node = nd.youngest(self.root)[1]
			grow_node.grow(self.age)
			bend_node = nd.random_child(self.root)
			if (bend_node != None):
				if nd.count(bend_node.left) < nd.count(bend_node.right):
					bend_node.left.bend(1)
				else:
					bend_node.right.bend(-1)

		self.update_surfaces()

	def update_surfaces(self):
		# Clear and make sure surfaces can be transparent
		self.surface.fill((0, 0, 0, 0))
		self.branches.fill((0, 0, 0, 0))
		self.leaves.fill((0, 0, 0, 0))

		# Draw branches and leaves onto respective surfaces
		nd.draw_branches(self.root, (180, 430), self.branches)
		nd.draw_leaves(self.root, (180, 430), self.leaves)
		leaves = pixellate_and_outline(self.leaves, pygame.Color(68, 94, 52, 255))

		# Draw shadow, then branches, then leaves to final surface
		shadow_pos, shadow_surf = shadow(leaves, pygame.Color(0, 0, 0, 100))
		self.surface.blit(pixellate(shadow_surf), (0, (400 - (shadow_pos[1] // 1.6))))
		self.surface.blit(pixellate_and_outline(self.branches, pygame.Color(79, 58, 28, 255)), (0, 0))
		self.surface.blit(leaves, (0, 0))

	def draw(self, surface: pygame.Surface, pos: tuple):
		surface.blit(self.surface, pos)




# Tree and tree drawing functions
def pixellate(surface: pygame.Surface) -> pygame.Surface:
	width, height = surface.get_size()
	small = pygame.transform.scale(surface, (width // 4, height // 4))
	return pygame.transform.scale(small, (width, height))


def pixellate_and_outline(surface: pygame.Surface, color: pygame.Color) -> pygame.Surface:
	width, height = surface.get_size()
	small = pygame.transform.scale(surface, (width // 4, height // 4))
	outlined = outline(small, color)
	return pygame.transform.scale(outlined, (width, height))


def outline(surface: pygame.Surface, color: pygame.Color) -> pygame.Surface:
	outline = pygame.mask.from_surface(surface)
	outline_size = outline.get_size()
	cropped_outline = pygame.mask.Mask((outline_size[0] - 1, outline_size[1] - 1))
	cropped_outline.draw(outline, (0, 0))
	outline.draw(cropped_outline, (1, 0))
	outline.draw(cropped_outline, (0, 1))
	outline.draw(cropped_outline, (-1, 0))
	outline.draw(cropped_outline, (0, -1))
	final = outline.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
	final.blit(surface, (0, 0))
	return final


def shadow(surface: pygame.Surface, color: pygame.Color) -> tuple[tuple[int, int], pygame.Surface]: # Returns the center of the shadow and the shadow
	mask = pygame.mask.from_surface(surface)
	shadow = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
	return (mask.centroid(), pygame.transform.scale(shadow, (shadow.get_width(), shadow.get_height() / 1.6)))