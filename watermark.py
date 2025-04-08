from PIL import ImageDraw, ImageFont

# Map font names to system-compatible TTF files
FONT_FILES = {
    "Arial": "arial.ttf",
    "Courier": "cour.ttf",
    "Times New Roman": "times.ttf",
    "Helvetica": "arial.ttf",  # Fallback
    "Comic Sans MS": "comic.ttf"
}

def add_watermark_to_image(image, text, font_name="Arial", font_size=30):
    watermarked = image.copy()
    draw = ImageDraw.Draw(watermarked)

    # Get the correct font file or fallback
    font_file = FONT_FILES.get(font_name, "arial.ttf")

    try:
        font = ImageFont.truetype(font_file, font_size)
    except:
        font = ImageFont.load_default()

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = (watermarked.width - text_width - 10, watermarked.height - text_height - 10)

    draw.text(position, text, font=font, fill=(255, 255, 255, 128))
    return watermarked
