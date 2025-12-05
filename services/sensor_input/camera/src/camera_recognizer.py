"""
CameraRecognizer module for camera-based activity recognition.

Responsibilities:
- Capture video frames from camera
- Detect and classify activity
- Return activity results
"""

import torch
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class CameraRecognizer:
    def __init__(self):
        """
        Initialize the CameraRecognizer module with YOLOS-Tiny model.
        """
        self.status = "initializing"
        self.processor = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        try:
            logger.info(f"Loading YOLOS-Tiny model on {self.device}...")
            self.processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
            self.model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")
            self.model.to(self.device)
            self.status = "ready"
            logger.info("YOLOS-Tiny model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load YOLOS-Tiny model: {e}")
            self.status = f"error: {e}"

    def recognize_activity(self, frame_data) -> dict:
        """
        Legacy method for general activity recognition.
        """
        # Placeholder detection logic
        detected_activity = None
        confidence = 0.0

        if isinstance(frame_data, list) and frame_data:
            frame_data = frame_data[0]

        if frame_data is not None:
            detected_activity = "motion_detected"
            confidence = 0.75

        return {"activity": detected_activity, "confidence": confidence}

    def detect_objects(self, frame) -> list:
        """
        Detect objects in a single frame using DETR.
        
        Args:
            frame: numpy array (CV2 frame, BGR)
            
        Returns:
            list: List of detected objects [{'label': str, 'score': float, 'box': [x1, y1, x2, y2]}]
        """
        if self.status != "ready" or frame is None:
            return []

        try:
            # Convert BGR (OpenCV) to RGB (PIL)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            inputs = self.processor(images=image, return_tensors="pt")
            inputs = inputs.to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Convert outputs (bounding boxes and class logits) to COCO API
            # let's only keep detections with score > 0.5
            target_sizes = torch.tensor([image.size[::-1]]).to(self.device)
            results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.5)[0]

            detections = []
            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                box = [round(i, 2) for i in box.tolist()]
                label_name = self.model.config.id2label[label.item()]
                detections.append({
                    "label": label_name,
                    "score": round(score.item(), 2),
                    "box": box
                })
            
            return detections

        except Exception as e:
            logger.error(f"Object detection error: {e}")
            return []

    def health_check(self) -> dict:
        """
        Return module health status.
        """
        return {"module": "CameraRecognizer", "status": self.status}


# Example usage
if __name__ == "__main__":
    recognizer = CameraRecognizer()
    # Create a dummy image
    dummy_frame = np.zeros((360, 640, 3), dtype=np.uint8)
    print("Health check:", recognizer.health_check())
    # results = recognizer.detect_objects(dummy_frame) # Might fail on empty black image with high threshold
    # print("Detections:", results)
