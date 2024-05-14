import pygame
import math
import random
from node import Node
from leaf import Leaf


brown0 = (133, 94, 41)
brown1 = (102, 68, 20)




def copy(node):
	if node is None:
		return None
	new_node = Node(node.age, node.length, node.angle)
	new_node.left = copy(node.left)
	new_node.right = copy(node.right)
	return new_node


def count(node: Node) -> int: # Returns the number of child nodes (incudes itself)
	if (node == None):
		return 0
	
	return 1 + count(node.left) + count(node.right)


def youngest(node: Node) -> tuple[int, Node]: # Returns the age and node
	if (node == None):
		return [10000, None]
		
	left = youngest(node.left)
	right = youngest(node.right)

	if (node.age < left[0] and node.age < right[0]):
		return (node.age, node)
	else:
		return left if left[0] < right[0] else right


def get_position(start: tuple[float ,float], radius: float, angle: float): # Takes rectangular and polar coords and adds them
	return ((start[0] + (radius * math.cos(angle))), (start[1] - (radius * math.sin(angle))))


def draw_parallel_lines(start, stop, perp_angle, width, window): # Perp angle needs to be in radians https://www.desmos.com/calculator/hh236r60m7
	for i in range(round(-width / 2), round(width / 2) + 1, 1):
		new_start = (start[0] + (i * math.cos(perp_angle)), start[1] + (-i * math.sin(perp_angle)) - (abs(i)**(2/3)))
		new_stop = (stop[0] + (i * math.cos(perp_angle)), stop[1] + (-i * math.sin(perp_angle)) + (abs(i)**(2/3)))
		
		if i < -1:
			brown = brown1
		else:
			brown = brown0
		pygame.draw.line(window, brown, new_start, new_stop, 3)


def draw_branches(node: Node, start: tuple[float, float], window: pygame.Surface) -> None: # Draws every node in a tree, along with connections
	if (node == None):
		return
	pos = get_position(start, node.length, math.radians(node.angle))
	width = count(node)**(3/4)

	pygame.draw.circle(window, brown0, pos, width * 0.6) # This brown circle colors in gaps between braches that are very bent
	draw_parallel_lines(start, pos, math.radians(node.angle + 90), width, window) # Draws the branch for each node
	# pygame.draw.line(window, (255, 255, 255), start, pos, 2) # Skeleton of the tree for testing purposes
	draw_branches(node.left, pos, window) # Recursively draws node's left and right children
	draw_branches(node.right, pos, window)


def draw_leaves(node: Node, start: tuple[float, float], window: pygame.Surface) -> None: # Draws every node in a tree, along with connections
	if (node == None):
		return
	pos = get_position(start, node.length, math.radians(node.angle))

	if (count(node) < 6): window.blit(node.leaves, (pos[0] - 32, pos[1] - 32)) # If the node has < 10 children draw leaves
	draw_leaves(node.left, pos, window) # Recursively draws node's left and right children
	draw_leaves(node.right, pos, window)
	if (count(node) < 4): window.blit(node.leaves, (pos[0] - 32, pos[1] - 32)) # If the node is extremely close to the edge, it also draws leaves on top
		

def random_child(node: Node) -> Node: # Picks a random node from the children of a root
	if (node == None or node.left == None or node.right == None):
		return None
	
	choices = [node, random_child(node.left), random_child(node.left), random_child(node.right), random_child(node.right)]
	return random.choice([valid for valid in choices if valid != None]) # Only returns valid choices (Not None and having 2 children)


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


class Tree:

	def __init__(self) -> None:
		self.age = 0
		self.rect = pygame.Rect(0, 0, 360, 460)
		self.branches = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.leaves = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.root = Node(self.age, 26, 90)

	def grow(self):
		if (count(self.root) < 50):
			self.age += 1
			grow_node = youngest(self.root)[1]
			grow_node.grow(self.age)
			bend_node = random_child(self.root)
			if (bend_node != None):
				if count(bend_node.left) < count(bend_node.right):
					bend_node.left.bend(1)
				else:
					bend_node.right.bend(-1)

		self.update_surfaces()

	def update_surfaces(self):
		# Make sure all surfaces can have transparencies
		self.surface.fill((0, 0, 0, 0))
		self.branches.fill((0, 0, 0, 0))
		self.leaves.fill((0, 0, 0, 0))

		# Draw branches and leaves onto respective surfaces
		draw_branches(self.root, (180, 430), self.branches)
		draw_leaves(self.root, (180, 430), self.leaves)
		leaves = pixellate_and_outline(self.leaves, pygame.Color(68, 94, 52, 255))

		# Draw shadow, then branches, then leaves to final surface
		shadow_pos, shadow_surf = shadow(leaves, pygame.Color(0, 0, 0, 100))
		self.surface.blit(pixellate(shadow_surf), (0, (400 - (shadow_pos[1] // 1.6))))
		self.surface.blit(pixellate_and_outline(self.branches, pygame.Color(79, 58, 28, 255)), (0, 0))
		self.surface.blit(leaves, (0, 0))

	def draw(self, surface: pygame.Surface, pos: tuple):
		surface.blit(self.surface, pos)