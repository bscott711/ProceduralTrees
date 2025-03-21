"""
Tree Module

This module defines the Tree class and related utility functions for generating procedural trees.
"""

import pygame
from typing import Dict, Tuple
import node as nd
import constants as cts


class Tree:
    """
    Represents a procedural tree with branches, leaves, and a shadow effect.

    Attributes:
        palette (Dict[str, Tuple[int, int, int]]): A dictionary of colors used for the tree.
        max_nodes (int): The maximum number of nodes allowed in the tree.
        age (int): The current age of the tree (used for growth).
        rect (pygame.Rect): The bounding rectangle for the tree's surface.
        branches (pygame.Surface): Surface for drawing tree branches.
        leaves (pygame.Surface): Surface for drawing tree leaves.
        surface (pygame.Surface): Final composite surface for the tree.
        root (Node): The root node of the tree.
    """

    def __init__(self, palette: Dict[str, Tuple[int, int, int]], max_nodes: int) -> None:
        """
        Initialize a new Tree instance.

        Args:
            palette (Dict[str, Tuple[int, int, int]]): A dictionary of colors for the tree.
            max_nodes (int): The maximum number of nodes in the tree.
        """
        self.palette = palette
        self.max_nodes = max_nodes
        self.age = 0
        self.rect = pygame.Rect(0, 0, cts.tree_surface_width, cts.tree_surface_height)
        self.branches = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.leaves = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.root = nd.Node(
            self.age, cts.start_branch_len, cts.start_branch_angle, self.palette
        )

    def grow(self) -> bool:
        """
        Grow the tree by adding new nodes and bending existing branches.

        Returns:
            bool: True if the tree grew, False if it has reached its maximum size.
        """
        if nd.count(self.root) < self.max_nodes:
            self.age += 1
            grow_node = nd.youngest(self.root)[1]
            grow_node.grow(self.age)

            bend_node = nd.random_child(self.root)
            if bend_node is not None:
                if nd.count(bend_node.left) < nd.count(bend_node.right):
                    bend_node.left.bend(1)
                else:
                    bend_node.right.bend(-1)

            self.update_surfaces()
            return True

        self.update_surfaces()
        return False

    def update_surfaces(self) -> None:
        """
        Update the tree's surfaces by redrawing branches, leaves, and shadows.
        """
        # Clear surfaces and ensure transparency
        self.surface.fill((0, 0, 0, 0))
        self.branches.fill((0, 0, 0, 0))
        self.leaves.fill((0, 0, 0, 0))

        # Draw branches and leaves onto respective surfaces
        nd.draw_branches(self.root, cts.tree_base_pos, self.branches)
        nd.draw_leaves(self.root, cts.tree_base_pos, self.leaves)
        leaves = pixellate_and_outline(self.leaves, self.palette["leaves_outline"])

        # Draw shadow, then branches, then leaves to the final surface
        shadow_pos, shadow_surf = shadow(leaves, self.palette["shadow_color"])
        self.surface.blit(
            pixellate(shadow_surf),
            (0, (cts.shadow_base - (shadow_pos[1] // cts.leaves_shadow_ratio))),
        )
        self.surface.blit(
            pixellate_and_outline(self.branches, self.palette["trunk_outline"]), (0, 0)
        )
        self.surface.blit(leaves, (0, 0))

    def draw(self, surface: pygame.Surface, pos: Tuple[int, int]) -> None:
        """
        Draw the tree onto a given surface at a specified position.

        Args:
            surface (pygame.Surface): The target surface to draw on.
            pos (Tuple[int, int]): The position (x, y) to draw the tree.
        """
        surface.blit(self.surface, pos)

    def change_color(self, new_palette: Dict[str, Tuple[int, int, int]]) -> None:
        """
        Change the tree's color palette.

        Args:
            new_palette (Dict[str, Tuple[int, int, int]]): A new dictionary of colors for the tree.
        """
        nd.change_palette(self.root, new_palette)


def pixellate(surface: pygame.Surface) -> pygame.Surface:
    """
    Apply a pixelation effect to a surface.

    Args:
        surface (pygame.Surface): The input surface.

    Returns:
        pygame.Surface: The pixelated surface.
    """
    width, height = surface.get_size()
    small = pygame.transform.scale(surface, (width // 4, height // 4))
    return pygame.transform.scale(small, (width, height))


def pixellate_and_outline(surface: pygame.Surface, color: pygame.Color) -> pygame.Surface:
    """
    Apply a pixelation effect and outline to a surface.

    Args:
        surface (pygame.Surface): The input surface.
        color (pygame.Color): The color for the outline.

    Returns:
        pygame.Surface: The pixelated and outlined surface.
    """
    width, height = surface.get_size()
    small = pygame.transform.scale(surface, (width // 4, height // 4))
    outlined = outline(small, color)
    return pygame.transform.scale(outlined, (width, height))


def outline(surface: pygame.Surface, color: pygame.Color) -> pygame.Surface:
    """
    Add an outline to a surface.

    Args:
        surface (pygame.Surface): The input surface.
        color (pygame.Color): The color for the outline.

    Returns:
        pygame.Surface: The outlined surface.
    """
    mask = pygame.mask.from_surface(surface)
    outline_size = mask.get_size()
    cropped_outline = pygame.mask.Mask((outline_size[0] - 1, outline_size[1] - 1))
    cropped_outline.draw(mask, (0, 0))
    mask.draw(cropped_outline, (1, 0))
    mask.draw(cropped_outline, (0, 1))
    mask.draw(cropped_outline, (-1, 0))
    mask.draw(cropped_outline, (0, -1))
    final = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
    final.blit(surface, (0, 0))
    return final


def shadow(
    surface: pygame.Surface, color: pygame.Color
) -> Tuple[Tuple[int, int], pygame.Surface]:
    """
    Create a shadow effect for a surface.

    Args:
        surface (pygame.Surface): The input surface.
        color (pygame.Color): The color for the shadow.

    Returns:
        Tuple[Tuple[int, int], pygame.Surface]: The centroid of the shadow and the shadow surface.
    """
    mask = pygame.mask.from_surface(surface)
    shadow_surf = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
    return (
        mask.centroid(),
        pygame.transform.scale(
            shadow_surf,
            (shadow_surf.get_width(), shadow_surf.get_height() // cts.leaves_shadow_ratio),
        ),
    )