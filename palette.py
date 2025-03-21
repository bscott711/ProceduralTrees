"""
Palette Module

This module provides utilities for loading, saving, and managing color palettes stored in a JSON file.
"""

import json
from typing import Dict, Tuple


FILENAME = "palettes.json"


class CustomEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to format lists more compactly by reducing indentation.

    This makes the JSON output easier to read while keeping lists concise.
    """

    def encode(self, obj) -> str:
        # Use the default JSON encoding
        json_str = super().encode(obj)

        # Post-process the JSON string to reduce list indentation
        json_str = json_str.replace("[\n            ", "[")
        json_str = json_str.replace("\n            ", " ")
        json_str = json_str.replace("\n        ]", "]")

        return json_str


def load() -> Dict[str, Dict[str, Tuple[int, int, int, int]]]:
    """
    Load all palettes from the JSON file.

    Each palette is a dictionary where keys are color names and values are RGBA tuples.

    Returns:
        Dict[str, Dict[str, Tuple[int, int, int, int]]]: A dictionary of palettes.
    """
    try:
        with open(FILENAME, "r") as file:
            palettes = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{FILENAME}' not found. Please ensure the file exists.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file '{FILENAME}'.")

    # Convert each color value (list) to a tuple
    return {
        palette: {color: tuple(palettes[palette][color]) for color in palettes[palette]}
        for palette in palettes
    }


def load_palette(name: str) -> Dict[str, Tuple[int, int, int, int]]:
    """
    Load a specific palette by name from the JSON file.

    Args:
        name (str): The name of the palette to load.

    Returns:
        Dict[str, Tuple[int, int, int, int]]: A dictionary where keys are color names and values are RGBA tuples.

    Raises:
        KeyError: If the specified palette does not exist.
    """
    palettes = load()
    if name not in palettes:
        raise KeyError(f"Palette '{name}' not found in '{FILENAME}'.")
    return palettes[name]


def save_palette(name: str, colors: Dict[str, Tuple[int, int, int, int]]) -> None:
    """
    Save a new or updated palette to the JSON file.

    Args:
        name (str): The name of the palette.
        colors (Dict[str, Tuple[int, int, int, int]]): A dictionary where keys are color names and values are RGBA tuples.

    Raises:
        ValueError: If the input colors are not valid RGBA tuples.
    """
    # Validate that all colors are valid RGBA tuples
    for color_name, color_value in colors.items():
        if (
            not isinstance(color_value, tuple)
            or len(color_value) != 4
            or not all(isinstance(c, int) for c in color_value)
        ):
            raise ValueError(f"Invalid RGBA value for color '{color_name}': {color_value}")

    # Convert tuples to lists for JSON serialization
    colors_serializable = {color: list(colors[color]) for color in colors}

    # Load existing palettes and update them
    try:
        palettes = load()
    except FileNotFoundError:
        palettes = {}

    palettes[name] = colors_serializable

    # Serialize and save the updated palettes
    json_data = json.dumps(palettes, cls=CustomEncoder, indent=4)
    try:
        with open(FILENAME, "w") as file:
            file.write(json_data)
    except IOError:
        raise IOError(f"Failed to write to file '{FILENAME}'.")