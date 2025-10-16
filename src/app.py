# Main application file for image annotation app
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import cv2
from annotation import draw_bounding_box, save_annotations
from utils import normalize_image

class AnnotationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotation App")
        
        # Variables
        self.image_folder = ""
        self.images = []
        self.current_image_index = 0
        self.current_image = None
        self.annotations = []
        
        # GUI Components
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Folder", command=self.load_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Canvas for image display
        self.canvas = tk.Canvas(root, width=800, height=600, bg="gray")
        self.canvas.pack()
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack()
        
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(button_frame, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.LEFT)
        
        self.save_button = tk.Button(button_frame, text="Save Annotations", command=self.save_annotations)
        self.save_button.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = tk.Label(root, text="No folder loaded")
        self.status_label.pack()

    def load_folder(self):
        self.image_folder = filedialog.askdirectory()
        if self.image_folder:
            self.images = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if self.images:
                self.current_image_index = 0
                self.load_image()
                self.status_label.config(text=f"Loaded {len(self.images)} images")
            else:
                messagebox.showwarning("No Images", "No image files found in the selected folder.")

    def load_image(self):
        if self.images:
            image_path = os.path.join(self.image_folder, self.images[self.current_image_index])
            self.current_image = Image.open(image_path)
            self.display_image()

    def display_image(self):
        if self.current_image:
            # Resize if necessary
            self.current_image.thumbnail((800, 600))
            self.photo = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def prev_image(self):
        if self.images and self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()

    def next_image(self):
        if self.images and self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.load_image()

    def save_annotations(self):
        if self.annotations:
            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filepath:
                save_annotations(self.annotations, filepath)
                messagebox.showinfo("Saved", "Annotations saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotationApp(root)
    root.mainloop()