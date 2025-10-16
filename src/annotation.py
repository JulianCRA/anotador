# Annotation functions
import cv2
import json
import numpy as np
from PIL import Image

def draw_bounding_box(image, bbox, label="", color=(255, 0, 0)):
    """
    Draw bounding box on PIL image.
    bbox: [x1, y1, x2, y2]
    """
    if isinstance(image, Image.Image):
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        cv_image = image.copy()
    
    x1, y1, x2, y2 = bbox
    cv2.rectangle(cv_image, (x1, y1), (x2, y2), color, 2)
    if label:
        cv2.putText(cv_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    if isinstance(image, Image.Image):
        return Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    return cv_image

def save_annotations(annotations, filepath, format_type="JSON"):
    """
    Save annotations to file.
    annotations: list of dicts [{'bbox': [x1,y1,x2,y2], 'label': str}]
    """
    if format_type == "JSON":
        with open(filepath, 'w') as f:
            json.dump(annotations, f, indent=4)
    # Add other formats if needed

def load_annotations(filepath, format_type="JSON"):
    """
    Load annotations from file.
    """
    if format_type == "JSON":
        with open(filepath, 'r') as f:
            return json.load(f)
    return []

def create_bounding_box(x1, y1, x2, y2, label="object"):
    """
    Create a bounding box annotation.
    """
    return {'bbox': [x1, y1, x2, y2], 'label': label}