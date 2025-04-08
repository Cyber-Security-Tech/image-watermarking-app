from tkinter import (
    Tk, Frame, Canvas, Button, Entry, StringVar, OptionMenu,
    Scale, HORIZONTAL, colorchooser, Label, messagebox, Scrollbar, VERTICAL, Y, BOTH, RIGHT, LEFT, NW
)
from PIL import ImageTk, ImageDraw, ImageFont
from file_manager import load_image, save_image
from watermark import add_watermark_to_image


class WatermarkApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Image Watermarking App")
        self.window.configure(bg="white")

        self.original_image = None
        self.watermarked_image = None
        self.selected_color = (255, 255, 255)

        # === Scrollable Canvas Setup ===
        outer_frame = Frame(window, bg="white")
        outer_frame.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(outer_frame, bg="white", highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(outer_frame, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", self._resize_canvas)

        # === Inner Frame (UI content) ===
        self.inner_frame = Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor=NW)

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # === Content ===
        self._build_ui(self.inner_frame)

    def _resize_canvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_ui(self, root):
        self.preview_canvas = Canvas(root, width=500, height=500, bg="lightgray")
        self.preview_canvas.pack(pady=(20, 10))

        self.upload_btn = Button(root, text="Upload Image", command=self.upload_image, width=25)
        self.upload_btn.pack(pady=5)

        self.watermark_entry = Entry(root, width=40)
        self.watermark_entry.insert(0, "Your Watermark")
        self.watermark_entry.pack(pady=5)

        font_size_frame = Frame(root, bg="white")
        font_size_frame.pack(pady=5)

        Label(font_size_frame, text="Font:", bg="white").grid(row=0, column=0, padx=10, pady=(0, 5))
        self.font_var = StringVar(value="Arial")
        font_options = ["Arial", "Courier", "Times New Roman", "Helvetica", "Comic Sans MS"]
        self.font_menu = OptionMenu(font_size_frame, self.font_var, *font_options)
        self.font_menu.grid(row=1, column=0, padx=10)

        Label(font_size_frame, text="Size:", bg="white").grid(row=0, column=1, padx=10, pady=(0, 5))
        self.size_slider = Scale(font_size_frame, from_=10, to=80, orient=HORIZONTAL, length=150)
        self.size_slider.set(30)
        self.size_slider.grid(row=1, column=1, padx=10)

        color_opacity_frame = Frame(root, bg="white")
        color_opacity_frame.pack(pady=5)

        Label(color_opacity_frame, text="Color:", bg="white").grid(row=0, column=0, padx=10, pady=(0, 5))
        self.color_btn = Button(color_opacity_frame, text="Pick Color", command=self.choose_color, width=15)
        self.color_btn.grid(row=1, column=0, padx=10)

        Label(color_opacity_frame, text="Opacity:", bg="white").grid(row=0, column=1, padx=10, pady=(0, 5))
        self.opacity_slider = Scale(color_opacity_frame, from_=0, to=255, orient=HORIZONTAL, length=150)
        self.opacity_slider.set(128)
        self.opacity_slider.grid(row=1, column=1, padx=10)

        button_frame = Frame(root, bg="white")
        button_frame.pack(pady=20)

        self.add_btn = Button(button_frame, text="Add Watermark", width=20, command=self.apply_watermark)
        self.add_btn.grid(row=0, column=0, padx=15)

        self.save_btn = Button(button_frame, text="Save Image", width=20, command=self.save_image)
        self.save_btn.grid(row=0, column=1, padx=15)

    def upload_image(self):
        self.original_image = load_image()
        self.watermarked_image = None
        if self.original_image:
            self.display_image(self.original_image)

    def display_image(self, img):
        self.preview_canvas.delete("all")
        photo = ImageTk.PhotoImage(img)
        self.preview_canvas.create_image(250, 250, image=photo)
        self.preview_canvas.image = photo

    def choose_color(self):
        color = colorchooser.askcolor(title="Pick a Text Color")
        if color[0]:
            self.selected_color = tuple(int(x) for x in color[0])

    def apply_watermark(self):
        if not self.original_image:
            messagebox.showerror("No Image", "Please upload an image first.")
            return

        text = self.watermark_entry.get()
        if not text:
            messagebox.showwarning("No Text", "Please enter watermark text.")
            return

        font_name = self.font_var.get()
        font_size = self.size_slider.get()
        opacity = self.opacity_slider.get()
        color = self.selected_color

        from PIL import Image, ImageDraw, ImageFont

        FONT_FILES = {
            "Arial": "arial.ttf",
            "Courier": "cour.ttf",
            "Times New Roman": "times.ttf",
            "Helvetica": "arial.ttf",
            "Comic Sans MS": "comic.ttf"
        }

        font_path = FONT_FILES.get(font_name, "arial.ttf")

        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # Create dummy image to calculate actual watermark box
        dummy_img = self.original_image.copy()
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), text, font=font)

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate centered position (same logic used in your add_watermark_to_image)
        x = (self.original_image.width - text_width) // 2
        y = (self.original_image.height - text_height) // 2

        # Check if watermark would go off the image
        if x < 0 or y < 0 or x + text_width > self.original_image.width or y + text_height > self.original_image.height:
            messagebox.showwarning(
                "Watermark May Be Cut Off",
                "Your watermark text might be cut off. Try reducing the font size or using a larger image."
            )

        self.watermarked_image = add_watermark_to_image(
            self.original_image, text, font_name, font_size, color, opacity
        )
        self.display_image(self.watermarked_image)



    def save_image(self):
        if not self.watermarked_image:
            messagebox.showerror("No Watermark", "Please add a watermark before saving.")
            return
        save_image(self.watermarked_image)
