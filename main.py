"""
Procedural Tree Generator

This script generates procedural trees using Pygame and OpenCV. It allows users to:
- Generate new trees.
- Save the current tree as an image.
- Export a video of the tree growth process.
- Change the tree's color palette dynamically using a dropdown menu.
"""

import pygame
import cv2
import numpy as np
from palette import load_palette
from tree import Tree


def create_button(width: int, height: int, text: str) -> pygame.Surface:
    """
    Create a button surface with rounded corners and centered text.

    Args:
        width (int): Width of the button.
        height (int): Height of the button.
        text (str): Text to display on the button.

    Returns:
        pygame.Surface: A Pygame surface containing the button.
    """
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(button_surface, (255, 255, 255), (0, 0, width, height), 0, 8)
    pygame.draw.rect(button_surface, (55, 55, 55), (0, 0, width, height), 4, 8)

    font = pygame.font.Font('freesansbold.ttf', 14)  # Reduced font size to 14
    text_surface = font.render(text, True, (55, 55, 55))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + 2))
    button_surface.blit(text_surface, text_rect)

    return button_surface


def save_tree_image(surface: pygame.Surface, filename: str) -> None:
    """
    Save a Pygame surface as an image file.

    Args:
        surface (pygame.Surface): The surface to save.
        filename (str): The name of the output file.
    """
    pygame.image.save(surface, filename)
    print(f"Image saved as {filename}")


def save_growth_video(frames: list[np.ndarray], size: tuple[int, int], fps: int, filename: str) -> None:
    """
    Save a list of frames as a video file.

    Args:
        frames (list[np.ndarray]): List of frames (as NumPy arrays).
        size (tuple[int, int]): Dimensions of the video (width, height).
        fps (int): Frames per second for the video.
        filename (str): The name of the output video file.
    """
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(filename, fourcc, fps, size)

    try:
        for frame in frames:
            frame = np.transpose(frame, (1, 0, 2))  # Pygame surface is transposed
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video_writer.write(frame)
        print(f"Video saved as {filename}")
    finally:
        video_writer.release()


def draw_dropdown(window, dropdown_rect, options, selected_option):
    """
    Draw a simulated dropdown menu.

    Args:
        window (pygame.Surface): The main game window.
        dropdown_rect (pygame.Rect): The rectangle defining the dropdown area.
        options (list[str]): The list of palette options.
        selected_option (str): The currently selected option.

    Returns:
        pygame.Rect: The rendered dropdown menu rectangle.
    """
    font = pygame.font.Font('freesansbold.ttf', 14)
    pygame.draw.rect(window, (255, 255, 255), dropdown_rect, 0, 8)
    pygame.draw.rect(window, (55, 55, 55), dropdown_rect, 4, 8)

    # Render the selected option
    text_surface = font.render(selected_option, True, (55, 55, 55))
    text_rect = text_surface.get_rect(center=dropdown_rect.center)
    window.blit(text_surface, text_rect)

    return dropdown_rect


def main():
    """
    Main function to run the procedural tree generator.
    """
    # Initialize Pygame
    pygame.init()

    # Window setup
    window_size = (400, 600)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Procedural Tree Generator")

    # Load default palette and initialize the tree
    default_palette_name = "green"
    selected_palette = default_palette_name
    palette = load_palette(selected_palette)
    tree = Tree(palette, 50)

    # Create buttons
    new_tree_button_surf = create_button(100, 50, "New Tree")
    new_tree_button_rect = pygame.Rect(20, 20, 100, 50)
    save_button_surf = create_button(100, 50, "Save")
    save_button_rect = pygame.Rect(window_size[0] - 120, 20, 100, 50)

    # Dropdown menu setup
    palette_options = ["green", "autumn", "cherry", "custom0", "custom1", "custom2"]
    dropdown_rect = pygame.Rect(
        (window_size[0] - 150) // 2, 20, 150, 50
    )  # Centered dropdown

    # Background image
    image = pygame.Surface(tree.surface.size, pygame.SRCALPHA)
    image.fill((130, 170, 70, 255))

    # Video settings
    video_fps = 60
    frames = []

    # Main loop
    running = True
    dropdown_expanded = False
    while running:
        # Grow the tree and capture frames
        if tree.grow():
            new_image = image.copy()
            new_image.blit(tree.surface, (0, 0))
            frames.append(pygame.surfarray.array3d(new_image))

        # Draw everything
        window.fill((130, 170, 70))
        tree.draw(window, (0, 0))
        window.blit(new_tree_button_surf, new_tree_button_rect)
        window.blit(save_button_surf, save_button_rect)

        # Draw dropdown menu
        dropdown_rect = draw_dropdown(window, dropdown_rect, palette_options, selected_palette)

        # Draw expanded dropdown options if active
        if dropdown_expanded:
            for i, option in enumerate(palette_options):
                option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.bottom + i * 30, dropdown_rect.width, 30)
                pygame.draw.rect(window, (255, 255, 255), option_rect, 0, 8)
                pygame.draw.rect(window, (55, 55, 55), option_rect, 2, 8)

                font = pygame.font.Font('freesansbold.ttf', 14)
                text_surface = font.render(option, True, (55, 55, 55))
                text_rect = text_surface.get_rect(center=option_rect.center)
                window.blit(text_surface, text_rect)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle "New Tree" button
                if new_tree_button_rect.collidepoint(event.pos):
                    tree = Tree(load_palette(selected_palette), 50)
                    frames.clear()
                    print("Generating new tree...")
                # Handle "Save" button
                elif save_button_rect.collidepoint(event.pos):
                    # Save the current tree image
                    new_image = image.copy()
                    new_image.blit(tree.surface, (0, 0))
                    save_tree_image(new_image, 'tree.png')

                    # Save the growth video
                    save_growth_video(frames, tree.surface.size, video_fps, "video.mp4")
                # Handle dropdown menu toggle
                elif dropdown_rect.collidepoint(event.pos):
                    dropdown_expanded = not dropdown_expanded
                # Handle dropdown option selection
                elif dropdown_expanded:
                    for i, option in enumerate(palette_options):
                        option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.bottom + i * 30, dropdown_rect.width, 30)
                        if option_rect.collidepoint(event.pos):
                            selected_palette = option
                            dropdown_expanded = False
                            try:
                                new_palette = load_palette(selected_palette)
                                tree.change_color(new_palette)
                                print(f"Changed tree color to '{selected_palette}' palette.")
                            except KeyError as e:
                                print(f"Error: {e}")

    pygame.quit()


if __name__ == "__main__":
    main()