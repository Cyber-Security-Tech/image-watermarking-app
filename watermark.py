from PIL import ImageDraw, ImageFont

def add_watermark_to_image(image, text, font_size=30):
    watermarked = image.copy()
    draw = ImageDraw.Draw(watermarked)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = (watermarked.width - text_width - 10, watermarked.height - text_height - 10)

    draw.text(position, text, font=font, fill=(255, 255, 255, 128))
    return watermarked
