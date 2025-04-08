from tkinter import (
    Canvas, Button, Entry, filedialog, messagebox,
    StringVar, OptionMenu, Scale, HORIZONTAL
)
from PIL import ImageTk
from file_manager import load_image, save_image
from watermark import add_watermark_to_image

class WatermarkApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Image Watermarking App")
        self.window.config(padx=20, pady=20)

        self.uploaded_image = None
        self.watermarked_image = None

        self.canvas = Canvas(width=500, height=500, bg="lightgray")
        self.canvas.pack()

        self.upload_btn = Button(text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        self.watermark_entry = Entry(width=30)
        self.watermark_entry.pack(pady=5)
        self.watermark_entry.insert(0, "Your Watermark")

        # --- Font selector ---
        self.font_var = StringVar(value="Arial")
        font_options = ["Arial", "Courier", "Times New Roman", "Helvetica", "Comic Sans MS"]
        self.font_menu = OptionMenu(window, self.font_var, *font_options)
        self.font_menu.pack(pady=5)

        # --- Font size slider ---
        self.size_slider = Scale(window, from_=10, to=80, orient=HORIZONTAL, label="Font Size")
        self.size_slider.set(30)
        self.size_slider.pack(pady=5)

        self.add_btn = Button(text="Add Watermark", command=self.apply_watermark)
        self.add_btn.pack(pady=5)

        self.save_btn = Button(text="Save Image", command=self.save_image)
        self.save_btn.pack(pady=10)

    def upload_image(self):
        self.uploaded_image = load_image()
        self.watermarked_image = None
        if self.uploaded_image:
            self.display_image(self.uploaded_image)

    def display_image(self, img):
        self.canvas.delete("all")  # Clear previous image
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(250, 250, image=photo)
        self.canvas.image = photo

    def apply_watermark(self):
        if not self.uploaded_image:
            messagebox.showerror("No Image", "Please upload an image first.")
            return

        text = self.watermark_entry.get()
        if not text:
            messagebox.showwarning("No Text", "Please enter watermark text.")
            return

        font_name = self.font_var.get()
        font_size = self.size_slider.get()

        # Always apply to original image, not already watermarked one
        self.watermarked_image = add_watermark_to_image(self.uploaded_image, text, font_name, font_size)
        self.display_image(self.watermarked_image)

    def save_image(self):
        if not self.watermarked_image:
            messagebox.showerror("No Watermark", "Please add a watermark before saving.")
            return
        save_image(self.watermarked_image)
