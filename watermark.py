from PIL import ImageDraw, ImageFont

FONT_FILES = {
    "Arial": "arial.ttf",
    "Courier": "cour.ttf",
    "Times New Roman": "times.ttf",
    "Helvetica": "arial.ttf",  # Fallback
    "Comic Sans MS": "comic.ttf"
}

def add_watermark_to_image(image, text, font_name="Arial", font_size=30, color=(255, 255, 255), opacity=128):
    watermarked = image.copy()
    draw = ImageDraw.Draw(watermarked)

    font_file = FONT_FILES.get(font_name, "arial.ttf")
    try:
        font = ImageFont.truetype(font_file, font_size)
    except:
        font = ImageFont.load_default()

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = (watermarked.width - text_width - 10, watermarked.height - text_height - 10)

    rgba_color = (*color, opacity)  # (R, G, B, A)
    draw.text(position, text, font=font, fill=rgba_color)
    return watermarked
