import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np

class GrayscaleExample:
    def __init__(self, root):
        self.root = root
        self.root.title("PIL Grayscale Example")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create image display area
        self.display_frame = ttk.LabelFrame(self.main_frame, text="Image Display")
        self.display_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Original image label
        self.original_label = ttk.Label(self.display_frame, text="Original Image")
        self.original_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.original_image_label = ttk.Label(self.display_frame)
        self.original_image_label.grid(row=1, column=0, padx=10, pady=5)
        
        # Grayscale image label
        self.gray_label = ttk.Label(self.display_frame, text="Grayscale Image")
        self.gray_label.grid(row=0, column=1, padx=10, pady=5)
        
        self.gray_image_label = ttk.Label(self.display_frame)
        self.gray_image_label.grid(row=1, column=1, padx=10, pady=5)
        
        # Controls frame
        self.controls_frame = ttk.LabelFrame(self.main_frame, text="Controls")
        self.controls_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        
        # Create sample image button
        self.create_button = ttk.Button(self.controls_frame, text="Create Sample Image", 
                                        command=self.create_sample_image)
        self.create_button.pack(pady=10)
        
        # Method selection
        self.method_label = ttk.Label(self.controls_frame, text="Grayscale Method:")
        self.method_label.pack(pady=(10, 5))
        
        self.method_var = tk.StringVar(value="pil")
        
        ttk.Radiobutton(self.controls_frame, text="PIL Method", 
                        variable=self.method_var, value="pil").pack(anchor=tk.W)
        ttk.Radiobutton(self.controls_frame, text="OpenCV Method", 
                        variable=self.method_var, value="opencv").pack(anchor=tk.W)
        ttk.Radiobutton(self.controls_frame, text="NumPy Method", 
                        variable=self.method_var, value="numpy").pack(anchor=tk.W)
        
        # Convert button
        self.convert_button = ttk.Button(self.controls_frame, text="Convert to Grayscale", 
                                         command=self.convert_to_grayscale)
        self.convert_button.pack(pady=10)
        
        # Initialize with a sample image
        self.create_sample_image()
        
    def create_sample_image(self):
        """Create a sample color image"""
        # Create a sample color image (a gradient with some shapes)
        width, height = 300, 300
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create a gradient background
        for y in range(height):
            for x in range(width):
                image[y, x] = [
                    int(255 * x / width),
                    int(255 * y / height),
                    int(255 * (1 - (x + y) / (width + height)))
                ]
        
        # Draw a red circle
        cv2.circle(image, (width//4, height//4), 50, (0, 0, 255), -1)
        
        # Draw a green rectangle
        cv2.rectangle(image, (width//2, height//2), (width-50, height-50), (0, 255, 0), -1)
        
        # Draw a blue triangle
        pts = np.array([[width//2, height//4], [width//4*3, height//4], [width//2, height//2]], np.int32)
        cv2.fillPoly(image, [pts], (255, 0, 0))
        
        self.original_np_image = image
        
        # Convert to PIL Image for display
        self.original_pil_image = PIL.Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        self.display_original_image()
        
    def display_original_image(self):
        """Display the original image"""
        # Convert PIL image to PhotoImage
        photo = PIL.ImageTk.PhotoImage(self.original_pil_image)
        
        # Update label
        self.original_image_label.configure(image=photo)
        self.original_image_label.image = photo  # Keep a reference
        
    def convert_to_grayscale(self):
        """Convert the image to grayscale using the selected method"""
        method = self.method_var.get()
        
        if method == "pil":
            # PIL method - convert to grayscale using PIL
            gray_image = self.original_pil_image.convert('L')
            # Convert back to RGB mode for display consistency
            gray_image_rgb = PIL.Image.merge('RGB', (gray_image, gray_image, gray_image))
            
        elif method == "opencv":
            # OpenCV method - convert to grayscale using cv2.cvtColor
            # First convert PIL to numpy array
            np_image = np.array(self.original_pil_image)
            # Convert RGB to BGR (OpenCV format)
            bgr_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
            # Convert to grayscale
            gray_np = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            # Convert back to RGB for display
            gray_rgb = cv2.cvtColor(gray_np, cv2.COLOR_GRAY2RGB)
            # Convert to PIL Image
            gray_image_rgb = PIL.Image.fromarray(gray_rgb)
            
        elif method == "numpy":
            # NumPy method - convert to grayscale using weighted average
            np_image = np.array(self.original_pil_image)
            # Apply grayscale formula: 0.299*R + 0.587*G + 0.114*B
            gray_np = np.dot(np_image[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)
            # Stack the grayscale channel to create an RGB image
            gray_rgb = np.stack([gray_np, gray_np, gray_np], axis=2)
            # Convert to PIL Image
            gray_image_rgb = PIL.Image.fromarray(gray_rgb)
        
        # Convert to PhotoImage for display
        photo = PIL.ImageTk.PhotoImage(gray_image_rgb)
        
        # Update label
        self.gray_image_label.configure(image=photo)
        self.gray_image_label.image = photo  # Keep a reference

if __name__ == "__main__":
    root = tk.Tk()
    app = GrayscaleExample(root)
    root.mainloop()