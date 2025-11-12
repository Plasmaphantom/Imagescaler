import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from datetime import datetime

class ImageScalerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Scaler")
        self.root.geometry("400x600")

        self.image_path = None
        self.original_dimensions = None
        self.scaled_image = None

        # GUI Elements
        self.label = tk.Label(root, text="Image Scaler", font=("Arial", 14))
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.dimension_label = tk.Label(root, text="Dimensions: Not loaded", font=("Arial", 10))
        self.dimension_label.pack(pady=5)

        self.scale_frame = tk.LabelFrame(root, text="Scaling Options", font=("Arial", 10))
        self.scale_frame.pack(pady=10, padx=10, fill="x")

        # 2x Scale (Up)
        self.scale_2x_frame = tk.Frame(self.scale_frame)
        self.scale_2x_frame.pack(pady=5, fill="x")
        self.scale_2x_button = tk.Button(self.scale_2x_frame, text="Scale Up 2x", command=lambda: self.scale_image(2.0))
        self.scale_2x_button.pack(side="left")
        self.scale_2x_label = tk.Label(self.scale_2x_frame, text="", font=("Arial", 10))
        self.scale_2x_label.pack(side="left", padx=10)

        # 0.5x Scale (Down)
        self.scale_05x_frame = tk.Frame(self.scale_frame)
        self.scale_05x_frame.pack(pady=5, fill="x")
        self.scale_05x_button = tk.Button(self.scale_05x_frame, text="Scale Down 0.5x", command=lambda: self.scale_image(0.5))
        self.scale_05x_button.pack(side="left")
        self.scale_05x_label = tk.Label(self.scale_05x_frame, text="", font=("Arial", 10))
        self.scale_05x_label.pack(side="left", padx=10)

        # 3x Scale (Up)
        self.scale_3x_frame = tk.Frame(self.scale_frame)
        self.scale_3x_frame.pack(pady=5, fill="x")
        self.scale_3x_button = tk.Button(self.scale_3x_frame, text="Scale Up 3x", command=lambda: self.scale_image(3.0))
        self.scale_3x_button.pack(side="left")
        self.scale_3x_label = tk.Label(self.scale_3x_frame, text="", font=("Arial", 10))
        self.scale_3x_label.pack(side="left", padx=10)

        # 0.33x Scale (Down)
        self.scale_033x_frame = tk.Frame(self.scale_frame)
        self.scale_033x_frame.pack(pady=5, fill="x")
        self.scale_033x_button = tk.Button(self.scale_033x_frame, text="Scale Down 0.33x", command=lambda: self.scale_image(0.333))
        self.scale_033x_button.pack(side="left")
        self.scale_033x_label = tk.Label(self.scale_033x_frame, text="", font=("Arial", 10))
        self.scale_033x_label.pack(side="left", padx=10)

        # Custom Scale
        self.custom_scale_label = tk.Label(self.scale_frame, text="Custom Scale (e.g., 0.5 for 50%):")
        self.custom_scale_label.pack(pady=5)
        self.custom_scale_entry = tk.Entry(self.scale_frame)
        self.custom_scale_entry.pack(pady=5)
        self.custom_scale_entry.bind("<KeyRelease>", self.update_custom_scale_label)
        self.custom_scale_result_label = tk.Label(self.scale_frame, text="", font=("Arial", 10))
        self.custom_scale_result_label.pack(pady=5)
        self.scale_custom_button = tk.Button(self.scale_frame, text="Apply Custom Scale", command=self.apply_custom_scale)
        self.scale_custom_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Scaled Image", command=self.save_image)
        self.save_button.pack(pady=10)
        self.save_button.config(state="disabled")

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if self.image_path:
            self.load_image(self.image_path)

    def load_image(self, path):
        try:
            image = Image.open(path)
            self.original_dimensions = image.size
            self.dimension_label.config(text=f"Original: {self.original_dimensions[0]} x {self.original_dimensions[1]}")
            self.update_scale_labels()
            self.save_button.config(state="normal")
            image.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def update_scale_labels(self):
        if self.original_dimensions:
            w, h = self.original_dimensions
            self.scale_2x_label.config(text=f"({int(w*2)} x {int(h*2)})")
            self.scale_05x_label.config(text=f"({int(w*0.5)} x {int(h*0.5)})")
            self.scale_3x_label.config(text=f"({int(w*3)} x {int(h*3)})")
            self.scale_033x_label.config(text=f"({int(w*0.333)} x {int(h*0.333)})")
            self.update_custom_scale_label()

    def update_custom_scale_label(self, event=None):
        if self.original_dimensions:
            try:
                scale_factor = float(self.custom_scale_entry.get() or 1.0)
                w, h = self.original_dimensions
                self.custom_scale_result_label.config(text=f"({int(w*scale_factor)} x {int(h*scale_factor)})")
            except ValueError:
                self.custom_scale_result_label.config(text="Invalid scale")

    def scale_image(self, scale_factor):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return

        try:
            image = Image.open(self.image_path)
            new_width = int(self.original_dimensions[0] * scale_factor)
            new_height = int(self.original_dimensions[1] * scale_factor)
            self.scaled_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            messagebox.showinfo("Success", f"Image scaled to {new_width} x {new_height}")
            image.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scale image: {e}")

    def apply_custom_scale(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return

        try:
            scale_factor = float(self.custom_scale_entry.get())
            if scale_factor <= 0:
                raise ValueError("Scale factor must be positive")
            self.scale_image(scale_factor)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for custom scale")

    def save_image(self):
        if not self.scaled_image:
            messagebox.showwarning("Warning", "No scaled image to save!")
            return

        output_dir = "scaled_images"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"scaled_image_{timestamp}.png")

        try:
            self.scaled_image.save(output_path, quality=95)
            messagebox.showinfo("Success", f"Image saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageScalerApp(root)
    root.mainloop()