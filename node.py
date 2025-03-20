"""
Node Module

This module defines the Node class and related utility functions for generating procedural trees.
"""

import math
import random
import pygame
from typing import Dict, Optional, Tuple
import constants as cts
from leaves import Leaves


class Node:
    """
    Represents a node in a procedural tree.

    Attributes:
        age (int): The age of the node (used for growth).
        length (int): The length of the branch.
        angle (int): The angle of the branch (in degrees).
        palette (Dict[str, Tuple[int, int, int]]): A dictionary of colors for the node.
        leaves (Leaves): The leaves associated with this node.
        left (Optional[Node]): The left child node.
        right (Optional[Node]): The right child node.
    """

    def __init__(self, age: int, length: int, angle: int, palette: Dict[str, Tuple[int, int, int]]) -> None:
        """
        Initialize a new Node instance.

        Args:
            age (int): The initial age of the node.
            length (int): The initial length of the branch.
            angle (int): The initial angle of the branch (in degrees).
            palette (Dict[str, Tuple[int, int, int]]): A dictionary of colors for the node.
        """
        self.age = age
        self.length = length
        self.angle = angle
        self.palette = palette
        self.leaves = Leaves(self.palette)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def add_left(self, age: int) -> None:
        """
        Add a left child node.

        Args:
            age (int): The age of the parent node.
        """
        length = max(random.randint(cts.min_length, cts.max_length) - age, cts.min_length)
        angle = random.randint(cts.min_angle_left, cts.max_angle_left)
        self.left = Node(age * 2, length, angle, self.palette)

    def add_right(self, age: int) -> None:
        """
        Add a right child node.

        Args:
            age (int): The age of the parent node.
        """
        length = max(random.randint(cts.min_length, cts.max_length) - age, cts.min_length)
        angle = random.randint(cts.min_angle_right, cts.max_angle_right)
        self.right = Node(age * 2, length, angle, self.palette)

    def grow(self, age: int) -> None:
        """
        Grow the node by adding children or increasing its length.

        Args:
            age (int): The current age of the tree.
        """
        number = random.randint(1, 3)
        if number == 1 and self.left is None:
            self.add_left(age)
        elif number == 2 and self.right is None:
            self.add_right(age)
        else:
            self.length += cts.grow_length_change
            self.age += cts.grow_age_change

    def bend(self, angle_increment: float) -> None:
        """
        Bend the branch by adjusting its angle.

        Args:
            angle_increment (float): The amount to adjust the angle.
        """
        if self.angle > cts.max_angle_left or self.angle < cts.min_angle_right:
            return
        self.angle += angle_increment
        self.age += cts.bend_age_change
        if self.left is not None:
            self.left.age += cts.bend_age_change
        if self.right is not None:
            self.right.age += cts.bend_age_change

    def change_color(self, new_palette: Dict[str, Tuple[int, int, int]]) -> None:
        """
        Change the node's color palette.

        Args:
            new_palette (Dict[str, Tuple[int, int, int]]): A new dictionary of colors.
        """
        self.palette = new_palette
        self.leaves.palette = self.palette
        self.leaves.generate_surface()


def copy(node: Optional[Node]) -> Optional[Node]:
    """
    Recursively copy a node and its children.

    Args:
        node (Optional[Node]): The node to copy.

    Returns:
        Optional[Node]: A deep copy of the node.
    """
    if node is None:
        return None
    new_node = Node(node.age, node.length, node.angle, node.palette)
    new_node.left = copy(node.left)
    new_node.right = copy(node.right)
    return new_node


def count(node: Optional[Node]) -> int:
    """
    Count the total number of nodes in a tree.

    Args:
        node (Optional[Node]): The root node of the tree.

    Returns:
        int: The total number of nodes.
    """
    if node is None:
        return 0
    return 1 + count(node.left) + count(node.right)


def youngest(node: Optional[Node]) -> Tuple[int, Optional[Node]]:
    """
    Find the youngest node in a tree.

    Args:
        node (Optional[Node]): The root node of the tree.

    Returns:
        Tuple[int, Optional[Node]]: The age and the youngest node.
    """
    if node is None:
        return 10000, None

    left_age, left_node = youngest(node.left)
    right_age, right_node = youngest(node.right)

    if node.age < left_age and node.age < right_age:
        return node.age, node
    return (left_age, left_node) if left_age < right_age else (right_age, right_node)


def draw_parallel_lines(
    start: Tuple[float, float],
    stop: Tuple[float, float],
    perp_angle: float,
    width: float,
    palette: Dict[str, Tuple[int, int, int]],
    window: pygame.Surface,
) -> None:
    """
    Draw parallel lines to represent branches.

    Args:
        start (Tuple[float, float]): The starting point of the branch.
        stop (Tuple[float, float]): The ending point of the branch.
        perp_angle (float): The perpendicular angle (in radians).
        width (float): The width of the branch.
        palette (Dict[str, Tuple[int, int, int]]): A dictionary of colors.
        window (pygame.Surface): The surface to draw on.
    """
    for i in range(round(-width / 2), round(width / 2) + 1, 1):
        new_start = (
            start[0] + (i * math.cos(perp_angle)),
            start[1] + (-i * math.sin(perp_angle)) - (abs(i) ** (2 / 3)),
        )
        new_stop = (
            stop[0] + (i * math.cos(perp_angle)),
            stop[1] + (-i * math.sin(perp_angle)) + (abs(i) ** (2 / 3)),
        )
        brown = palette["trunk1"] if i < -1 else palette["trunk0"]
        pygame.draw.line(window, brown, new_start, new_stop, 3)


def get_position(start: Tuple[float, float], radius: float, angle: float) -> Tuple[float, float]:
    """
    Calculate the position of a point based on polar coordinates.

    Args:
        start (Tuple[float, float]): The starting point.
        radius (float): The distance from the starting point.
        angle (float): The angle (in radians).

    Returns:
        Tuple[float, float]: The calculated position.
    """
    return (
        start[0] + (radius * math.cos(angle)),
        start[1] - (radius * math.sin(angle)),
    )


def draw_branches(node: Optional[Node], start: Tuple[float, float], window: pygame.Surface) -> None:
    """
    Recursively draw all branches in a tree.

    Args:
        node (Optional[Node]): The current node.
        start (Tuple[float, float]): The starting point of the branch.
        window (pygame.Surface): The surface to draw on.
    """
    if node is None:
        return
    pos = get_position(start, node.length, math.radians(node.angle))
    width = count(node) ** cts.trunk_width_power

    pygame.draw.circle(window, node.palette["trunk0"], pos, width * 0.6)
    draw_parallel_lines(start, pos, math.radians(node.angle + 90), width, node.palette, window)
    draw_branches(node.left, pos, window)
    draw_branches(node.right, pos, window)


def draw_leaves(node: Optional[Node], start: Tuple[float, float], window: pygame.Surface) -> None:
    """
    Recursively draw all leaves in a tree.

    Args:
        node (Optional[Node]): The current node.
        start (Tuple[float, float]): The starting point of the branch.
        window (pygame.Surface): The surface to draw on.
    """
    if node is None:
        return
    pos = get_position(start, node.length, math.radians(node.angle))
    top_left_pos = (
        pos[0] - cts.leaf_surface_width / 2,
        pos[1] - cts.leaf_surface_height / 2,
    )

    if count(node) < cts.children_for_leaves:
        window.blit(node.leaves.surface, top_left_pos)
    draw_leaves(node.left, pos, window)
    draw_leaves(node.right, pos, window)


def random_child(node: Optional[Node]) -> Optional[Node]:
    """
    Select a random child node from the tree.

    Args:
        node (Optional[Node]): The root node of the tree.

    Returns:
        Optional[Node]: A randomly selected child node.
    """
    if node is None or node.left is None or node.right is None:
        return None

    choices = [
        node,
        random_child(node.left),
        random_child(node.left),
        random_child(node.right),
        random_child(node.right),
    ]
    return random.choice([valid for valid in choices if valid is not None])


def change_palette(node: Optional[Node], new_palette: Dict[str, Tuple[int, int, int]]) -> None:
    """
    Recursively change the color palette of a tree.

    Args:
        node (Optional[Node]): The root node of the tree.
        new_palette (Dict[str, Tuple[int, int, int]]): A new dictionary of colors.
    """
    if node is None:
        return
    node.change_color(new_palette)
    change_palette(node.right, new_palette)
    change_palette(node.left, new_palette)