import tkinter as tk

class KeyboardControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Control Example")
        self.root.geometry("400x300")
        
        # Create a canvas where we'll display a movable object
        self.canvas = tk.Canvas(root, width=400, height=200, bg="white")
        self.canvas.pack(pady=20)
        
        # Create a rectangle that will be controlled by keyboard
        self.rect = self.canvas.create_rectangle(180, 80, 220, 120, fill="blue")
        
        # Create a label to show pressed keys
        self.key_label = tk.Label(root, text="Press arrow keys to move the square\nPress 'c' to change color\nPress 'r' to reset position")
        self.key_label.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Status: Ready")
        self.status_label.pack(pady=5)
        
        # Bind keyboard events to the window
        self.root.bind("<Key>", self.key_press)
        
        # Set focus to the window so it can receive keyboard events
        self.root.focus_set()
        
        # Available colors for cycling
        self.colors = ["blue", "red", "green", "orange", "purple"]
        self.current_color = 0

    def key_press(self, event):
        """Handle keyboard events"""
        key = event.keysym
        
        # Update status label
        self.status_label.config(text=f"Status: Key pressed - {key}")
        
        # Move the rectangle based on arrow keys
        if key == "Left":
            self.canvas.move(self.rect, -10, 0)
        elif key == "Right":
            self.canvas.move(self.rect, 10, 0)
        elif key == "Up":
            self.canvas.move(self.rect, 0, -10)
        elif key == "Down":
            self.canvas.move(self.rect, 0, 10)
        # Change color when 'c' is pressed
        elif key.lower() == "c":
            self.current_color = (self.current_color + 1) % len(self.colors)
            self.canvas.itemconfig(self.rect, fill=self.colors[self.current_color])
        # Reset position when 'r' is pressed
        elif key.lower() == "r":
            self.canvas.coords(self.rect, 180, 80, 220, 120)
            self.canvas.itemconfig(self.rect, fill="blue")
            self.current_color = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardControlApp(root)
    root.mainloop()