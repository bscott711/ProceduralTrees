import random
from leaf import Leaf

class Node:
	
	def __init__(self, age: int, length: int, angle: int) -> None:
		self.age = age
		self.length = length
		self.angle = angle
		self.left = None
		self.right = None
		self.leaves = Leaf(age)

	def add_left(self, age) -> None:
		self.left = Node(age * 2, max(random.randint(15, 40) - age, 12), random.randint(95, 110))

	def add_right(self, age) -> None:
		self.right = Node(age * 2, max(random.randint(15, 40) - age, 12), random.randint(70, 85))

	def grow(self, age) -> None:
		number = random.randint(1, 3)
		if (number == 1 and self.left == None): self.add_left(age)
		elif (number == 2 and self.right == None): self.add_right(age)
		else:
			self.length += 2
			self.age += 13

	def bend(self, angle_incremeent: float):
		if self.angle > 140 or self.angle < 40:
			return
		self.angle += angle_incremeent
		self.age -= 3
		if self.left != None: self.left.age -= 3
		if self.right != None: self.right.age -= 3
