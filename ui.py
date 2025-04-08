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
        self.tk_image = None
        self.selected_color = (255, 255, 255)
        self.drag_position = None
        self.warning_shown = False

        outer_frame = Frame(window, bg="white")
        outer_frame.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(outer_frame, bg="white", highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(outer_frame, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", self._resize_canvas)

        self.inner_frame = Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor=NW)

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self._build_ui(self.inner_frame)

    def _resize_canvas(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_ui(self, root):
        self.preview_canvas = Canvas(root, width=500, height=500, bg="lightgray")
        self.preview_canvas.pack(pady=(20, 10))

        self.preview_canvas.bind("<Button-1>", self.start_drag)
        self.preview_canvas.bind("<B1-Motion>", self.do_drag)
        self.preview_canvas.bind("<ButtonRelease-1>", self.end_drag)

        Label(root, text="💡 Tip: Drag the watermark to reposition. Changes auto-preview.", bg="white", fg="gray").pack()

        self.upload_btn = Button(root, text="Upload Image", command=self.upload_image, width=25)
        self.upload_btn.pack(pady=5)

        self.watermark_entry = Entry(root, width=40)
        self.watermark_entry.insert(0, "Your Watermark")
        self.watermark_entry.pack(pady=5)
        self.watermark_entry.bind("<KeyRelease>", lambda e: self.apply_watermark())

        font_size_frame = Frame(root, bg="white")
        font_size_frame.pack(pady=5)

        Label(font_size_frame, text="Font:", bg="white").grid(row=0, column=0, padx=10, pady=(0, 5))
        self.font_var = StringVar(value="Arial")
        font_options = ["Arial", "Courier", "Times New Roman", "Helvetica", "Comic Sans MS"]
        self.font_menu = OptionMenu(font_size_frame, self.font_var, *font_options, command=lambda _: self.apply_watermark())
        self.font_menu.grid(row=1, column=0, padx=10)

        Label(font_size_frame, text="Size:", bg="white").grid(row=0, column=1, padx=10, pady=(0, 5))
        self.size_slider = Scale(font_size_frame, from_=10, to=80, orient=HORIZONTAL, length=150,
                                 command=lambda val: self.apply_watermark())
        self.size_slider.set(30)
        self.size_slider.grid(row=1, column=1, padx=10)

        color_opacity_frame = Frame(root, bg="white")
        color_opacity_frame.pack(pady=5)

        Label(color_opacity_frame, text="Color:", bg="white").grid(row=0, column=0, padx=10, pady=(0, 5))
        self.color_btn = Button(color_opacity_frame, text="Pick Color", command=self.choose_color, width=15)
        self.color_btn.grid(row=1, column=0, padx=10)

        Label(color_opacity_frame, text="Opacity:", bg="white").grid(row=0, column=1, padx=10, pady=(0, 5))
        self.opacity_slider = Scale(color_opacity_frame, from_=0, to=255, orient=HORIZONTAL, length=150,
                                    command=lambda val: self.apply_watermark())
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
        self.drag_position = None
        if self.original_image:
            self.display_image(self.original_image)
            self.apply_watermark()

    def display_image(self, img):
        self.preview_canvas.delete("all")
        self.tk_image = ImageTk.PhotoImage(img)
        self.preview_canvas.create_image(250, 250, image=self.tk_image)
        self.preview_canvas.image = self.tk_image

    def choose_color(self):
        color = colorchooser.askcolor(title="Pick a Text Color")
        if color[0]:
            self.selected_color = tuple(int(x) for x in color[0])
            self.apply_watermark()

    def start_drag(self, event):
        self.drag_position = (event.x, event.y)
        self.warning_shown = False
        self.apply_watermark()

    def do_drag(self, event):
        self.drag_position = (event.x, event.y)
        self.apply_watermark()

    def end_drag(self, event):
        self.drag_position = (event.x, event.y)
        self.apply_watermark()

    def apply_watermark(self):
        if not self.original_image:
            return

        text = self.watermark_entry.get()
        if not text:
            return

        font_name = self.font_var.get()
        font_size = self.size_slider.get()
        opacity = self.opacity_slider.get()
        color = self.selected_color

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

        dummy_img = self.original_image.copy()
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if self.drag_position:
            x = self.drag_position[0] - text_width // 2
            y = self.drag_position[1] - text_height // 2
        else:
            x = (self.original_image.width - text_width) // 2
            y = (self.original_image.height - text_height) // 2

        if x < 0 or y < 0 or x + text_width > self.original_image.width or y + text_height > self.original_image.height:
            if not self.warning_shown:
                self.warning_shown = True
                messagebox.showwarning(
                    "Watermark May Be Cut Off",
                    "Your watermark text might be cut off. Try reducing the font size or using a larger image."
                )

        self.watermarked_image = add_watermark_to_image(
            self.original_image, text, font_name, font_size, color, opacity, (x, y)
        )
        self.display_image(self.watermarked_image)

    def save_image(self):
        if not self.watermarked_image:
            messagebox.showerror("No Watermark", "Please add a watermark before saving.")
            return
        save_image(self.watermarked_image)
