"""
main.py – Entry point for the Image Watermarking App.

Initializes the main Tkinter window and starts the GUI event loop.
"""

from tkinter import Tk
from ui import WatermarkApp

def main():
    """Initialize the main application window and run the app."""
    window = Tk()
    window.title("Image Watermarking App")
    window.geometry("700x700")  # You can adjust this if needed
    app = WatermarkApp(window)
    window.mainloop()

if __name__ == "__main__":
    main()
