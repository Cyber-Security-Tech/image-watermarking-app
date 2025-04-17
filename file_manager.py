"""
file_manager.py – Handles image file loading and saving for the watermarking app.
"""

from tkinter import filedialog, messagebox
from PIL import Image

def load_image():
    """
    Open a file dialog and load an image from disk.
    
    Returns:
        PIL.Image or None: The loaded image, or None if no file selected.
    """
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((500, 500))  # Resize for preview purposes
        return img
    return None

def save_image(img):
    """
    Open a save dialog and export the provided image to disk.

    Args:
        img (PIL.Image): The image to save.
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")]
    )
    if file_path:
        try:
            img.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{e}")
