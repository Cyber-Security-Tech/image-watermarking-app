from tkinter import Tk
from ui import WatermarkApp

if __name__ == "__main__":
    window = Tk()
    window.title("Image Watermarking App")
    window.geometry("700x700")  
    app = WatermarkApp(window)
    window.mainloop()
