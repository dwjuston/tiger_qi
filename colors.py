from enum import Enum
import pygame

class GameColor(Enum):
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)
    GREEN = (0, 128, 0)
    LIGHT_BLUE = (173, 216, 230)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)

# Available colors for painting
AVAILABLE_COLORS = [
    GameColor.RED.value,
    GameColor.ORANGE.value,
    GameColor.YELLOW.value,
    GameColor.GREEN.value,
    GameColor.BLUE.value,
    GameColor.PURPLE.value,
    GameColor.LIGHT_BLUE.value
]

def combine_colors(color1: tuple[int, int, int], color2: tuple[int, int, int], ratio: float = 0.5) -> tuple[int, int, int]:
    """
    Combine two RGB colors with a specified ratio.
    
    Args:
        color1: First RGB color tuple (r, g, b)
        color2: Second RGB color tuple (r, g, b)
        ratio: Ratio of color1 to color2 (0.0 to 1.0). Default is 0.5 (equal mix)
    
    Returns:
        Combined RGB color tuple (r, g, b)
    """
    # Ensure ratio is between 0 and 1
    ratio = max(0.0, min(1.0, ratio))
    
    # Calculate the inverse ratio
    inv_ratio = 1.0 - ratio
    
    # Combine each channel
    r = int(color1[0] * ratio + color2[0] * inv_ratio)
    g = int(color1[1] * ratio + color2[1] * inv_ratio)
    b = int(color1[2] * ratio + color2[2] * inv_ratio)
    
    return (r, g, b)

# Example usage:
# red = GameColor.RED.value
# blue = GameColor.BLUE.value
# purple = combine_colors(red, blue, 0.5)  # Mix red and blue equally
# light_red = combine_colors(red, GameColor.WHITE.value, 0.7)  # 70% red, 30% white 