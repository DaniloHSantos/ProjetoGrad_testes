import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import os

class DrawingApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Drawing Application")
        
        # Initialize canvas dimensions
        self.canvas_width = 800
        self.canvas_height = 600
        
        # Main frame
        self.main_frame = ttk.Frame(window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height,
                               bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create blank image for drawing
        self.image = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        self.display_image()
        
        # Controls frame
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Drawing parameters
        self.drawing = False
        self.last_x = None
        self.last_y = None
        self.color = (0, 0, 0)  # Black color (BGR)
        self.thickness = 2
        
        # Tool selection
        self.tool_frame = ttk.LabelFrame(self.controls_frame, text="Tools")
        self.tool_frame.pack(fill=tk.X, pady=5)
        
        self.tool_var = tk.StringVar(value="pen")
        ttk.Radiobutton(self.tool_frame, text="Pen", variable=self.tool_var, 
                       value="pen").pack(anchor=tk.W)
        ttk.Radiobutton(self.tool_frame, text="Line", variable=self.tool_var, 
                       value="line").pack(anchor=tk.W)
        ttk.Radiobutton(self.tool_frame, text="Rectangle", variable=self.tool_var, 
                       value="rectangle").pack(anchor=tk.W)
        ttk.Radiobutton(self.tool_frame, text="Circle", variable=self.tool_var, 
                       value="circle").pack(anchor=tk.W)
        ttk.Radiobutton(self.tool_frame, text="Eraser", variable=self.tool_var, 
                       value="eraser").pack(anchor=tk.W)
        
        # Thickness control
        self.thickness_frame = ttk.LabelFrame(self.controls_frame, text="Thickness")
        self.thickness_frame.pack(fill=tk.X, pady=5)
        
        self.thickness_var = tk.IntVar(value=2)
        self.thickness_scale = ttk.Scale(self.thickness_frame, from_=1, to=20, 
                                       variable=self.thickness_var, orient=tk.HORIZONTAL)
        self.thickness_scale.pack(fill=tk.X, padx=5, pady=5)
        self.thickness_scale.bind("<ButtonRelease-1>", self.update_thickness)
        
        # Color selection
        self.color_frame = ttk.LabelFrame(self.controls_frame, text="Color")
        self.color_frame.pack(fill=tk.X, pady=5)
        
        self.color_button = tk.Button(self.color_frame, bg="black", width=6, height=2,
                                     command=self.choose_color)
        self.color_button.pack(padx=5, pady=5)
        
        # Action buttons
        self.action_frame = ttk.LabelFrame(self.controls_frame, text="Actions")
        self.action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(self.action_frame, text="Clear", command=self.clear_canvas).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.action_frame, text="Save", command=self.save_image).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(self.action_frame, text="Exit", command=self.window.quit).pack(fill=tk.X, padx=5, pady=2)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(window, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        # Keyboard shortcuts
        self.window.bind("<Control-z>", self.undo)
        self.window.bind("<Control-s>", self.save_image)
        self.window.bind("<Control-c>", self.clear_canvas)
        
        # History for undo
        self.history = [self.image.copy()]
        self.history_index = 0
        self.max_history = 10
    
    def display_image(self):
        """Convert OpenCV image to PhotoImage and display on canvas"""
        # Convert BGR to RGB for PIL
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        self.pil_image = PIL.Image.fromarray(rgb_image)
        
        # Convert to PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image=self.pil_image)
        
        # Clear canvas and display new image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
    
    def start_drawing(self, event):
        """Start drawing when mouse button is pressed"""
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        
        # For shape tools, save a copy of the current image
        tool = self.tool_var.get()
        if tool in ["line", "rectangle", "circle"]:
            self.temp_image = self.image.copy()
    
    def draw(self, event):
        """Draw on the image as the mouse moves"""
        if not self.drawing:
            return
        
        x, y = event.x, event.y
        tool = self.tool_var.get()
        
        # Update thickness from slider
        self.thickness = self.thickness_var.get()
        
        # Get color (BGR for OpenCV)
        color = self.color if tool != "eraser" else (255, 255, 255)
        
        if tool == "pen" or tool == "eraser":
            # Draw line from last position to current position
            cv2.line(self.image, (self.last_x, self.last_y), (x, y), color, self.thickness)
            self.last_x, self.last_y = x, y
            self.display_image()
            
        elif tool in ["line", "rectangle", "circle"]:
            # Create a copy of the original image
            temp_img = self.temp_image.copy()
            
            if tool == "line":
                cv2.line(temp_img, (self.last_x, self.last_y), (x, y), color, self.thickness)
            elif tool == "rectangle":
                cv2.rectangle(temp_img, (self.last_x, self.last_y), (x, y), color, self.thickness)
            elif tool == "circle":
                radius = int(((x - self.last_x) ** 2 + (y - self.last_y) ** 2) ** 0.5)
                cv2.circle(temp_img, (self.last_x, self.last_y), radius, color, self.thickness)
            
            # Update the display with the temporary image
            self.image = temp_img
            self.display_image()
    
    def stop_drawing(self, event):
        """Stop drawing when mouse button is released"""
        if self.drawing:
            self.drawing = False
            
            # Add current state to history for undo
            if len(self.history) >= self.max_history:
                self.history.pop(0)
            self.history.append(self.image.copy())
            self.history_index = len(self.history) - 1
            
            # Update status
            self.status_var.set(f"Drew with {self.tool_var.get()} at ({event.x}, {event.y})")
    
    def update_thickness(self, event):
        """Update line thickness from slider"""
        self.thickness = self.thickness_var.get()
        self.status_var.set(f"Thickness set to {self.thickness}")
    
    def choose_color(self):
        """Open color chooser dialog"""
        rgb_color, _ = colorchooser.askcolor(title="Choose Color")
        if rgb_color:
            # Update button color
            hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))
            self.color_button.config(bg=hex_color)
            
            # Store as BGR for OpenCV
            self.color = (int(rgb_color[2]), int(rgb_color[1]), int(rgb_color[0]))
            self.status_var.set(f"Color set to RGB: {rgb_color}")
    
    def clear_canvas(self, event=None):
        """Clear the canvas"""
        self.image = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        self.display_image()
        
        # Add to history
        if len(self.history) >= self.max_history:
            self.history.pop(0)
        self.history.append(self.image.copy())
        self.history_index = len(self.history) - 1
        
        self.status_var.set("Canvas cleared")
    
    def undo(self, event=None):
        """Undo the last action"""
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index].copy()
            self.display_image()
            self.status_var.set("Undo")
    
    def save_image(self, event=None):
        """Save the current image"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            cv2.imwrite(file_path, self.image)
            self.status_var.set(f"Image saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()