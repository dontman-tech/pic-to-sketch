import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

class PencilSketchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to sketch converter")
        self.root.geometry("600x600")
        
        # State variables
        self.original_cv_image = None
        self.sketch_cv_image = None
        self.tk_image = None
        
        # UI Setup
        self.setup_ui()
        
    def setup_ui(self):
        # Top Frame for buttons
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        self.upload_btn = tk.Button(top_frame, text="Upload Image", command=self.upload_image, font=("Arial", 12))
        self.upload_btn.pack(side=tk.LEFT, padx=10)
        
        self.save_btn = tk.Button(top_frame, text="Save Sketch", command=self.save_image, state=tk.DISABLED, font=("Arial", 12))
        self.save_btn.pack(side=tk.LEFT, padx=10)
        
        # Canvas Frame for displaying image
        self.canvas_frame = tk.Frame(self.root, bg="gray")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.image_label = tk.Label(self.canvas_frame, text="No Image Selected", bg="lightgray", font=("Arial", 14))
        self.image_label.pack(fill=tk.BOTH, expand=True)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not file_path:
            return
            
        # Read image using cv2
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Error", "Could not read the uploaded image.")
            return
        
        self.original_cv_image = img
        self.convert_to_sketch()

    def convert_to_sketch(self):
        if self.original_cv_image is None:
            return
            
        try:
            # 1. Convert to grayscale
            gray_img = cv2.cvtColor(self.original_cv_image, cv2.COLOR_BGR2GRAY)
            
            # 2. Invert the grayscale image
            inverted_img = cv2.bitwise_not(gray_img)
            
            # 3. Blur the inverted image
            blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), 0)
            
            # 4. Invert the blurred image
            inverted_blur = cv2.bitwise_not(blurred_img)
            
            # 5. Create the pencil sketch (Color Dodge blend mode)
            self.sketch_cv_image = cv2.divide(gray_img, inverted_blur, scale=256.0)
            
            self.display_image(self.sketch_cv_image)
            self.save_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while converting: {e}")

    def display_image(self, cv_img):
        # Convert cv2 grayscale image to PIL format
        pil_img = Image.fromarray(cv_img)
        
        # Calculate aspect ratio to fit within display area (e.g., 500x500 max)
        max_size = 500
        w, h = pil_img.size
        if w > max_size or h > max_size:
            if w > h:
                new_w = max_size
                new_h = int((h / w) * max_size)
            else:
                new_h = max_size
                new_w = int((w / h) * max_size)
            pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)
            
        # Convert PIL image to Tkinter image
        self.tk_image = ImageTk.PhotoImage(pil_img)
        
        # Update label
        self.image_label.config(image=self.tk_image, text="")

    def save_image(self):
        if self.sketch_cv_image is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            title="Save Sketch",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
        )
        if file_path:
            # Save using cv2
            success = cv2.imwrite(file_path, self.sketch_cv_image)
            if success:
                messagebox.showinfo("Success", f"Image saved successfully to:\n{file_path}")
            else:
                messagebox.showerror("Error", "Failed to save the image.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PencilSketchApp(root)
    root.mainloop()
