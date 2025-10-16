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
        self.annotations = {}  # key: image_name, value: list of annotations
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.bbox_items = []  # canvas items for bboxes
        
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
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack()
        
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = tk.Button(button_frame, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.LEFT)
        
        self.save_button = tk.Button(button_frame, text="Save Annotations", command=self.save_annotations)
        self.save_button.pack(side=tk.LEFT)
        
        # Label entry
        tk.Label(button_frame, text="Label:").pack(side=tk.LEFT)
        self.label_entry = tk.Entry(button_frame)
        self.label_entry.insert(0, "object")
        self.label_entry.pack(side=tk.LEFT)
        
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
        self.canvas.delete("all")  # Clear canvas
        self.bbox_items = []
        if self.current_image:
            # Resize if necessary
            self.current_image.thumbnail((800, 600))
            self.photo = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            # Draw existing annotations
            image_name = self.images[self.current_image_index]
            if image_name in self.annotations:
                for ann in self.annotations[image_name]:
                    bbox = ann['bbox']
                    label = ann['label']
                    item = self.canvas.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], outline="red", width=2)
                    self.bbox_items.append(item)
                    text_item = self.canvas.create_text(bbox[0], bbox[1]-10, text=label, anchor=tk.SW, fill="red")
                    self.bbox_items.append(text_item)

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
                # Flatten annotations for saving
                all_annotations = []
                for img, anns in self.annotations.items():
                    for ann in anns:
                        ann['image'] = img
                        all_annotations.append(ann)
                save_annotations(all_annotations, filepath)
                messagebox.showinfo("Saved", "Annotations saved successfully.")

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)

    def on_mouse_move(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        if self.rect and self.start_x is not None:
            x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
            x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
            label = self.label_entry.get()
            if label:
                image_name = self.images[self.current_image_index]
                if image_name not in self.annotations:
                    self.annotations[image_name] = []
                self.annotations[image_name].append({'bbox': [x1, y1, x2, y2], 'label': label})
                # Draw the bbox
                item = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
                self.bbox_items.append(item)
                text_item = self.canvas.create_text(x1, y1-10, text=label, anchor=tk.SW, fill="red")
                self.bbox_items.append(text_item)
        self.rect = None
        self.start_x = None
        self.start_y = None

if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotationApp(root)
    root.mainloop()