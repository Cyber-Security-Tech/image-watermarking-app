# 🖼️ Image Watermarking App

A full-featured desktop application built with Python and Tkinter that allows users to add text or logo watermarks to images with powerful customization options.

## 🚀 Features

- ✅ Upload any image and add a custom watermark
- ✅ Add either **text** or **logo** (or both!) as a watermark
- ✅ **Drag and drop** to reposition the watermark on the image
- ✅ Customize text:
  - Font family
  - Font size
  - Text color
  - Opacity
- ✅ Resize logos dynamically
- ✅ Add multiple layers: text + logo
- ✅ **Undo and Redo** support (with full action history)
- ✅ Smart warning if watermark might get cut off
- ✅ Transparent checkerboard background preview
- ✅ Scrollable responsive UI for smaller windows

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (for GUI)
- **Pillow (PIL)** (for image manipulation)

## 📚 What I Learned

This project helped solidify several key programming skills:
- 🧠 **Object-Oriented Design**: Structuring the app around a single `WatermarkApp` class with clearly scoped methods
- 🎨 **GUI Development**: Building scrollable, dynamic interfaces in Tkinter
- 🖼️ **Image Manipulation**: Using Pillow for watermarking, layering, transparency, and image resizing
- 🕹️ **Interactive UI Logic**: Implementing real-time drag-and-drop movement for both text and logos
- 🔁 **State Management**: Building a complete undo/redo system using stacks and deep copies of state
- 🧪 **Debugging & Testing**: Tracing tricky UI bugs and ensuring that all layout and rendering issues were fixed

## 💾 How to Run

1. Clone the repo:
```bash
git clone https://github.com/Cyber-Security-Tech/image-watermarking-app
```

2. Install dependencies:
```bash
pip install pillow
```

3. Run the app:
```bash
python main.py
```

## 📂 File Structure

- `main.py` / `ui.py` — Main app logic
- `file_manager.py` — Load/save helper functions
- `watermark.py` — Core watermark application logic
- `README.md` — This file

---

This project demonstrates practical GUI programming and real-world problem-solving with image processing.
