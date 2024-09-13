import pygame
import node as nd
import constants as cts

Node = nd.Node


class Tree:

	def __init__(self, palette: dict, max_nodes: int) -> None:
		self.palette = palette
		self.max_nodes = max_nodes
		self.age = 0
		self.rect = pygame.Rect(0, 0, cts.tree_surface_width, cts.tree_surface_height)
		self.branches = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.leaves = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.root = Node(self.age, cts.start_branch_len, cts.start_branch_angle, self.palette)

	def grow(self):
		if (nd.count(self.root) < self.max_nodes):
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
			return True
		
		self.update_surfaces()
		return False

	def update_surfaces(self):
		# Clear and make sure surfaces can be transparent
		self.surface.fill((0, 0, 0, 0))
		self.branches.fill((0, 0, 0, 0))
		self.leaves.fill((0, 0, 0, 0))

		# Draw branches and leaves onto respective surfaces
		nd.draw_branches(self.root, cts.tree_base_pos, self.branches)
		nd.draw_leaves(self.root, cts.tree_base_pos, self.leaves)
		leaves = pixellate_and_outline(self.leaves, self.palette["leaves_outline"])

		# Draw shadow, then branches, then leaves to final surface
		shadow_pos, shadow_surf = shadow(leaves, self.palette["shadow_color"])
		self.surface.blit(pixellate(shadow_surf), (0, (cts.shadow_base - (shadow_pos[1] // cts.leaves_shadow_ratio))))
		self.surface.blit(pixellate_and_outline(self.branches, self.palette["trunk_outline"]), (0, 0))
		self.surface.blit(leaves, (0, 0))

	def draw(self, surface: pygame.Surface, pos: tuple):
		surface.blit(self.surface, pos)

	def change_color(self, new_palette: dict):
		nd.change_palette(self.root, new_palette)




# Tree and surface functions
def pixellate(surface: pygame.Surface) -> pygame.Surface:
	width, height = surface.get_size()
	small = pygame.transform.scale(surface, (width // 4, height // 4))
	return pygame.transform.scale(small, (width, height))


def pixellate_and_outline(surface: pygame.Surface, color: pygame.Color) -> pygame.Surface:
	width, height = surface.get_size()
	small = pygame.transform.scale(surface, (width // 4, height // 4))
	outlined = outline(small, color)
	return pygame.transform.scale(outlined, (width, height))


# I have no clue why the mask has to be cropped slightly but just trust me
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
	return (mask.centroid(), pygame.transform.scale(shadow, (shadow.get_width(), shadow.get_height() / cts.leaves_shadow_ratio)))