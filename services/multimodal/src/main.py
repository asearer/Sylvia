"""
Entrypoint for the Multimodal Reasoning service.
Coordinates processing of images, diagrams, tables, and text.
"""

from diagram_parser import DiagramParser
from math_ocr import MathOCR
from table_extractor import TableExtractor
from image_captioner import ImageCaptioner
from fusion_engine import FusionEngine
import os

class MultimodalReasoning:
    def __init__(self):
        """
        Initialize all multimodal processing modules.
        """
        self.diagram_parser = DiagramParser()
        self.math_ocr = MathOCR()
        self.table_extractor = TableExtractor()
        self.image_captioner = ImageCaptioner()
        self.fusion_engine = FusionEngine()

    def process_image(self, image_path: str) -> dict:
        """
        Process an image across multiple modalities and return fused results.

        Args:
            image_path (str): Path to the image file.

        Returns:
            dict: Fused representation of diagrams, math, tables, and captions.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        diagrams = self.diagram_parser.parse(image_path)
        math_text = self.math_ocr.extract(image_path)
        tables = self.table_extractor.extract(image_path)
        captions = self.image_captioner.caption(image_path)

        fused_output = self.fusion_engine.fuse(diagrams, math_text, tables, captions)
        return fused_output

    def health_check(self) -> dict:
        """
        Return health status of all multimodal modules.

        Returns:
            dict: Module names and their health statuses.
        """
        return {
            "DiagramParser": self.diagram_parser.health_check(),
            "MathOCR": self.math_ocr.health_check(),
            "TableExtractor": self.table_extractor.health_check(),
            "ImageCaptioner": self.image_captioner.health_check(),
            "FusionEngine": self.fusion_engine.health_check()
        }

# Example usage
if __name__ == "__main__":
    mm = MultimodalReasoning()
    try:
        result = mm.process_image("sample.png")
        print("Fused multimodal output:", result)
    except FileNotFoundError as e:
        print(e)
    print("Health check:", mm.health_check())
