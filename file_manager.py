from tkinter import filedialog, messagebox
from PIL import Image

def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((500, 500))
        return img
    return None

def save_image(img):
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Image", "*.png")])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully!")
