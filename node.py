import pygame
import math
import random
import constants as cts
from leaves import Leaves


class Node:
	
	def __init__(self, age: int, length: int, angle: int, palette: dict) -> None:
		self.age = age
		self.length = length
		self.angle = angle
		self.palette = palette
		self.leaves = Leaves(self.palette)
		self.left = None
		self.right = None

	def add_left(self, age) -> None:
		length = max(random.randint(cts.min_length, cts.max_length) - age, cts.min_length)
		angle = random.randint(cts.min_angle_left, cts.max_angle_left)
		self.left = Node(age * 2, length, angle, self.palette) # Child nodes inherit the same palette

	def add_right(self, age) -> None:
		length = max(random.randint(cts.min_length, cts.max_length) - age, cts.min_length)
		angle = random.randint(cts.min_angle_right, cts.max_angle_right)
		self.right = Node(age * 2, length, angle, self.palette)

	def grow(self, age) -> None:
		number = random.randint(1, 3)
		if (number == 1 and self.left == None): self.add_left(age)
		elif (number == 2 and self.right == None): self.add_right(age)
		else:
			self.length += cts.grow_length_change
			self.age += cts.grow_age_change

	def bend(self, angle_incremeent: float):
		if self.angle > cts.max_angle_left or self.angle < cts.min_angle_right:
			return
		self.angle += angle_incremeent
		self.age += cts.bend_age_change
		if self.left != None: self.left.age += cts.bend_age_change
		if self.right != None: self.right.age += cts.bend_age_change

	def change_color(self, new_palette: dict):
		self.palette = new_palette
		self.leaves.palette = self.palette
		self.leaves.generate_surface()


# Node functions
def copy(node: Node) -> Node:
	if node is None:
		return None
	new_node = Node(node.age, node.length, node.angle, node.palette)
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


def draw_parallel_lines(start, stop, perp_angle, width, palette, window): # Perp angle needs to be in radians https://www.desmos.com/calculator/hh236r60m7
	for i in range(round(-width / 2), round(width / 2) + 1, 1):
		new_start = (start[0] + (i * math.cos(perp_angle)), start[1] + (-i * math.sin(perp_angle)) - (abs(i)**(2/3)))
		new_stop = (stop[0] + (i * math.cos(perp_angle)), stop[1] + (-i * math.sin(perp_angle)) + (abs(i)**(2/3)))
		brown = palette["trunk1"] if i < -1 else palette["trunk0"]
		pygame.draw.line(window, brown, new_start, new_stop, 3)


def get_position(start: tuple[float ,float], radius: float, angle: float): # Takes rectangular and polar coords and adds them
	return ((start[0] + (radius * math.cos(angle))), (start[1] - (radius * math.sin(angle))))


def draw_branches(node: Node, start: tuple[float, float], window: pygame.Surface) -> None: # Draws every node in a tree, along with connections
	if (node == None):
		return
	pos = get_position(start, node.length, math.radians(node.angle))
	width = count(node)**cts.trunk_width_power

	pygame.draw.circle(window, node.palette["trunk0"], pos, width * 0.6) # This brown circle colors in gaps between braches that are very bent
	draw_parallel_lines(start, pos, math.radians(node.angle + 90), width, node.palette, window) # Draws the branch for each node
	# pygame.draw.line(window, (255, 255, 255), start, pos, 2) # Skeleton of the tree for testing purposes
	# pygame.draw.circle(window, (255, 255, 255), pos, 6, 2)
	draw_branches(node.left, pos, window) # Recursively draws node's left and right children
	draw_branches(node.right, pos, window)


def draw_leaves(node: Node, start: tuple[float, float], window: pygame.Surface) -> None: # Draws every node in a tree, along with connections
	if (node == None):
		return
	pos = get_position(start, node.length, math.radians(node.angle))
	top_left_pos = (pos[0] - cts.leaf_surface_width / 2, pos[1] - cts.leaf_surface_height / 2)

	if (count(node) < cts.children_for_leaves): window.blit(node.leaves.surface, top_left_pos) # If the node has few enough children draw leaves
	draw_leaves(node.left, pos, window) # Recursively draws node's left and right children's leaves
	draw_leaves(node.right, pos, window)
		

def random_child(node: Node) -> Node: # Picks a random node from the children of a root
	if (node == None or node.left == None or node.right == None):
		return None
	
	choices = [node, random_child(node.left), random_child(node.left), random_child(node.right), random_child(node.right)]
	return random.choice([valid for valid in choices if valid != None]) # Only returns valid choices (Not None and having 2 children)


def change_palette(node: Node, new_palette: dict):
	if (node == None):
		return
	node.change_color(new_palette)
	change_palette(node.right, new_palette)
	change_palette(node.left, new_palette)
	