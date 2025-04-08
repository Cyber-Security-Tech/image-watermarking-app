from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

window = Tk()
window.title("Image Watermarking App")
window.config(padx=20, pady=20)

canvas = Canvas(width=500, height=500, bg="lightgray")
canvas.pack()

uploaded_image = None
watermarked_image = None

def upload_image():
    global uploaded_image, watermarked_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        uploaded_image = Image.open(file_path)
        uploaded_image.thumbnail((500, 500))
        watermarked_image = None
        display_image(uploaded_image)

def display_image(img):
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(250, 250, image=photo)
    canvas.image = photo

def add_watermark():
    global uploaded_image, watermarked_image
    if uploaded_image:
        text = watermark_entry.get()
        if not text:
            messagebox.showwarning("No Text", "Please enter watermark text.")
            return
        watermarked = uploaded_image.copy()
        draw = ImageDraw.Draw(watermarked)

        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()

        # Get text bounding box instead of using deprecated textsize
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (watermarked.width - text_width - 10, watermarked.height - text_height - 10)

        draw.text(position, text, font=font, fill=(255, 255, 255, 128))
        watermarked_image = watermarked
        display_image(watermarked_image)
    else:
        messagebox.showerror("No Image", "Please upload an image first.")

def save_image():
    global watermarked_image
    if watermarked_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png")])
        if file_path:
            watermarked_image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")
    else:
        messagebox.showerror("No Watermark", "Please add a watermark before saving.")

upload_btn = Button(text="Upload Image", command=upload_image)
upload_btn.pack(pady=10)

watermark_entry = Entry(width=30)
watermark_entry.pack(pady=5)
watermark_entry.insert(0, "Your Watermark")

add_btn = Button(text="Add Watermark", command=add_watermark)
add_btn.pack(pady=5)

save_btn = Button(text="Save Image", command=save_image)
save_btn.pack(pady=10)

window.mainloop()
