"""
watermark.py – Contains the logic for adding text watermarks to images.
"""

from PIL import ImageDraw, ImageFont

# Supported font display names mapped to local .ttf files
FONT_FILES = {
    "Arial": "arial.ttf",
    "Courier": "cour.ttf",
    "Times New Roman": "times.ttf",
    "Helvetica": "arial.ttf",  # fallback to Arial
    "Comic Sans MS": "comic.ttf"
}

def add_watermark_to_image(image, text, font_name, font_size, color, opacity, position=None):
    """
    Apply a text watermark to the given image.

    Args:
        image (PIL.Image): The input image.
        text (str): The watermark text.
        font_name (str): Name of the font to use.
        font_size (int): Size of the watermark text.
        color (tuple): RGB color tuple (e.g., (255, 255, 255)).
        opacity (int): Opacity level (0–255).
        position (tuple or None): (x, y) coordinates, or None to center text.

    Returns:
        PIL.Image: Image with watermark applied.
    """
    watermarked = image.copy()
    draw = ImageDraw.Draw(watermarked)

    # Load font (fallback if missing)
    font_path = FONT_FILES.get(font_name, "arial.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

    # Measure text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Determine position
    if position:
        x, y = position
    else:
        x = (image.width - text_width) // 2
        y = (image.height - text_height) // 2

    # Create RGBA color with opacity
    rgba_color = (*color, opacity)

    # Draw text
    draw.text((x, y), text, font=font, fill=rgba_color)

    return watermarked
