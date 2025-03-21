"""
Leaves Module

This module defines the Leaves class and related utility functions for generating and rendering 
the leaves of a procedural tree.
"""

import random
import pygame
from typing import Dict, Tuple


def random_pos() -> Tuple[int, int]:
    """
    Generate a random position within the bounds of the leaf surface.

    Returns:
        Tuple[int, int]: A random (x, y) position.
    """
    import constants as cts  # Import here to avoid circular dependencies
    return (
        random.randint(0, cts.leaf_surface_width),
        random.randint(0, cts.leaf_surface_height),
    )


def draw_leaf(surface: pygame.Surface, color: Tuple[int, int, int], pos: Tuple[int, int]) -> None:
    """
    Draw a single leaf on the given surface.

    Args:
        surface (pygame.Surface): The surface to draw on.
        color (Tuple[int, int, int]): The color of the leaf.
        pos (Tuple[int, int]): The position (x, y) of the leaf.
    """
    pygame.draw.rect(surface, color, (pos[0], pos[1], 12, 12))
    pygame.draw.rect(surface, color, (pos[0] + 4, pos[1] + 4, 12, 12))


class Leaves:
    """
    Represents the leaves of a procedural tree.

    Attributes:
        palette (Dict[str, Tuple[int, int, int]]): A dictionary of colors for the leaves.
        size (Tuple[int, int]): The dimensions of the leaf surface.
        surface (pygame.Surface): The surface used to render the leaves.
        leaves (list[list[Tuple[int, int]]]): A list of lists containing leaf positions.
    """

    def __init__(self, palette: Dict[str, Tuple[int, int, int]]) -> None:
        """
        Initialize a new Leaves instance.

        Args:
            palette (Dict[str, Tuple[int, int, int]]): A dictionary of colors for the leaves.
        """
        import constants as cts  # Import here to avoid circular dependencies
        self.palette = palette
        self.size = (cts.leaf_surface_width, cts.leaf_surface_height)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.leaves = [
            [random_pos() for _ in range(num_leaves)]
            for num_leaves in cts.leaves_density
        ]
        self.generate_surface()

    def generate_surface(self) -> None:
        """
        Generate the leaf surface by drawing all leaves with their respective colors.
        """
        self.surface.fill((0, 0, 0, 0))  # Clear the surface before redrawing
        for layer_index, layer in enumerate(self.leaves):
            color_key = f"leaves{layer_index}"
            if color_key not in self.palette:
                raise KeyError(f"Missing key '{color_key}' in palette.")
            for leaf_pos in layer:
                draw_leaf(self.surface, self.palette[color_key], leaf_pos)