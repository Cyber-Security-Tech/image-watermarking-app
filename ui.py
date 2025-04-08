from tkinter import (
    Tk, Frame, Canvas, Button, Entry, StringVar, Scale, HORIZONTAL, colorchooser,
    Label, messagebox, Scrollbar, VERTICAL, Y, BOTH, RIGHT, LEFT, NW, filedialog,
    Toplevel, Listbox, END
)
from PIL import Image, ImageTk, ImageDraw, ImageFont
from file_manager import load_image, save_image
from watermark import add_watermark_to_image

FONT_FILES = {
    "Arial": "arial.ttf",
    "Courier": "cour.ttf",
    "Times New Roman": "times.ttf",
    "Helvetica": "arial.ttf",
    "Comic Sans MS": "comic.ttf"
}


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
        self.logo_position = None
        self.logo_image = None
        self.logo_drag_active = False
        self.text_drag_active = False
        self.font_var = StringVar(value="Arial")
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
        self.preview_canvas = Canvas(root, width=500, height=500)
        self.preview_canvas.pack(pady=(20, 10))

        self.preview_canvas.bind("<Button-1>", self.start_drag)
        self.preview_canvas.bind("<B1-Motion>", self.do_drag)
        self.preview_canvas.bind("<ButtonRelease-1>", self.end_drag)

        Button(root, text="Upload Image", command=self.upload_image, width=25).pack(pady=5)

        self.watermark_entry = Entry(root, width=40)
        self.watermark_entry.insert(0, "Your Watermark")
        self.watermark_entry.pack(pady=5)
        self.watermark_entry.bind("<KeyRelease>", lambda e: self.apply_watermark())

        font_frame = Frame(root, bg="white")
        font_frame.pack(pady=5)

        Label(font_frame, text="Font:", bg="white").grid(row=0, column=0, padx=10)
        Button(font_frame, text="Choose Font", command=self.show_font_dropdown, width=15).grid(row=1, column=0, padx=10)

        Label(font_frame, text="Size:", bg="white").grid(row=0, column=1, padx=10)
        self.size_slider = Scale(font_frame, from_=10, to=80, orient=HORIZONTAL, length=150,
                                 command=lambda val: self.apply_watermark())
        self.size_slider.set(30)
        self.size_slider.grid(row=1, column=1, padx=10)

        color_frame = Frame(root, bg="white")
        color_frame.pack(pady=5)

        Label(color_frame, text="Color:", bg="white").grid(row=0, column=0, padx=10)
        self.color_btn = Button(color_frame, text="Pick Color", command=self.choose_color, width=15)
        self.color_btn.grid(row=1, column=0, padx=10)

        Label(color_frame, text="Opacity:", bg="white").grid(row=0, column=1, padx=10)
        self.opacity_slider = Scale(color_frame, from_=0, to=255, orient=HORIZONTAL, length=150,
                                    command=lambda val: self.apply_watermark())
        self.opacity_slider.set(128)
        self.opacity_slider.grid(row=1, column=1, padx=10)

        logo_frame = Frame(root, bg="white")
        logo_frame.pack(pady=10)

        Button(logo_frame, text="Upload Logo", command=self.upload_logo, width=20).grid(row=0, column=0, padx=10)
        Label(logo_frame, text="Logo Size (%):", bg="white").grid(row=0, column=1, padx=5)

        self.logo_slider = Scale(logo_frame, from_=10, to=100, orient=HORIZONTAL, length=150,
                                 command=lambda val: self.apply_watermark())
        self.logo_slider.set(30)
        self.logo_slider.grid(row=0, column=2, padx=5)

        button_frame = Frame(root, bg="white")
        button_frame.pack(pady=20)

        Button(button_frame, text="Add Watermark", width=18, command=self.apply_watermark).grid(row=0, column=0, padx=10)
        Button(button_frame, text="Save Image", width=18, command=self.save_image).grid(row=0, column=1, padx=10)

    def show_font_dropdown(self):
        if hasattr(self, "font_picker_win") and self.font_picker_win.winfo_exists():
            return

        self.font_picker_win = Toplevel(self.window)
        self.font_picker_win.title("Choose Font")
        self.font_picker_win.configure(bg="white")

        listbox = Listbox(self.font_picker_win, height=8, width=30)
        listbox.pack(padx=10, pady=10)

        self.font_list = list(FONT_FILES.keys())
        for i, font_name in enumerate(self.font_list):
            listbox.insert(END, font_name)
            try:
                listbox.itemconfig(i, {'font': (font_name, 14)})
            except:
                pass

        def select_font(event):
            idx = listbox.curselection()
            if idx:
                selected = self.font_list[idx[0]]
                self.font_var.set(selected)
                self.apply_watermark()

        listbox.bind("<<ListboxSelect>>", select_font)
        Button(self.font_picker_win, text="Close", command=self.font_picker_win.destroy).pack(pady=(0, 10))

    def upload_image(self):
        self.original_image = load_image().convert("RGBA")
        self.drag_position = None
        self.logo_position = None
        self.apply_watermark()

    def upload_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.logo_image = Image.open(path).convert("RGBA")
            self.logo_position = (250, 250)
            self.apply_watermark()

    def choose_color(self):
        color = colorchooser.askcolor(title="Pick a Text Color")
        if color[0]:
            self.selected_color = tuple(int(x) for x in color[0])
            self.apply_watermark()

    def start_drag(self, event):
        if self.logo_image:
            lx, ly = self.logo_position or (250, 250)
            logo_width = int(self.logo_image.width * self.logo_slider.get() / 100)
            logo_height = int(self.logo_image.height * self.logo_slider.get() / 100)
            if lx - logo_width // 2 <= event.x <= lx + logo_width // 2 and ly - logo_height // 2 <= event.y <= ly + logo_height // 2:
                self.logo_drag_active = True
                return
        self.text_drag_active = True

    def do_drag(self, event):
        if self.text_drag_active:
            self.drag_position = (event.x, event.y)
        elif self.logo_drag_active:
            self.logo_position = (event.x, event.y)
        self.apply_watermark()

    def end_drag(self, event):
        self.text_drag_active = False
        self.logo_drag_active = False

    def apply_watermark(self):
        if not self.original_image:
            return

        base = self.original_image.copy()
        draw = ImageDraw.Draw(base)

        # === Text ===
        text = self.watermark_entry.get()
        font_name = self.font_var.get()
        font_size = self.size_slider.get()
        opacity = self.opacity_slider.get()
        color = self.selected_color

        if text:
            font_path = FONT_FILES.get(font_name, "arial.ttf")
            try:
                font = ImageFont.truetype(font_path, font_size)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

            x, y = self.drag_position or ((base.width - w) // 2, (base.height - h) // 2)
            if x < 0 or y < 0 or x + w > base.width or y + h > base.height:
                if not self.warning_shown:
                    self.warning_shown = True
                    messagebox.showwarning("Watermark Cutoff", "Text watermark might be cut off.")

            txt_overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
            ImageDraw.Draw(txt_overlay).text((x, y), text, font=font, fill=color + (opacity,))
            base = Image.alpha_composite(base, txt_overlay)

        # === Logo ===
        if self.logo_image:
            scale = self.logo_slider.get() / 100
            resized = self.logo_image.resize((int(self.logo_image.width * scale), int(self.logo_image.height * scale)))
            lx, ly = self.logo_position or ((base.width - resized.width) // 2, (base.height - resized.height) // 2)
            overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
            overlay.paste(resized, (lx - resized.width // 2, ly - resized.height // 2), resized)
            base = Image.alpha_composite(base, overlay)

        self.watermarked_image = base
        self.display_image(base)

    def display_image(self, img):
        self.preview_canvas.delete("all")
        bg = Image.new("RGB", (500, 500), "white")
        draw = ImageDraw.Draw(bg)
        for y in range(0, 500, 20):
            for x in range(0, 500, 20):
                fill = (220, 220, 220) if (x//20 + y//20) % 2 == 0 else (255, 255, 255)
                draw.rectangle([x, y, x + 20, y + 20], fill=fill)
        composite = Image.alpha_composite(bg.convert("RGBA"), img.resize((500, 500)).convert("RGBA"))
        self.tk_image = ImageTk.PhotoImage(composite)
        self.preview_canvas.create_image(0, 0, anchor=NW, image=self.tk_image)
        self.preview_canvas.image = self.tk_image

    def save_image(self):
        if not self.watermarked_image:
            messagebox.showerror("No Watermark", "Please add a watermark first.")
            return
        save_image(self.watermarked_image)
