from PIL import ImageDraw, ImageFont

FONT_FILES = {
    "Arial": "arial.ttf",
    "Courier": "cour.ttf",
    "Times New Roman": "times.ttf",
    "Helvetica": "arial.ttf",
    "Comic Sans MS": "comic.ttf"
}

def add_watermark_to_image(image, text, font_name, font_size, color, opacity, position=None):
    watermarked = image.copy()
    draw = ImageDraw.Draw(watermarked)

    font_path = FONT_FILES.get(font_name, "arial.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Get size of the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Determine position: use drag-drop if given, else center
    if position:
        x, y = position
    else:
        x = (image.width - text_width) // 2
        y = (image.height - text_height) // 2

    # Apply watermark with specified opacity
    rgba_color = (*color, opacity)
    draw.text((x, y), text, font=font, fill=rgba_color)

    return watermarked
