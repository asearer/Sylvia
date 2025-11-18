"""
Entrypoint for the Multimodal Reasoning service.
Coordinates processing of images, diagrams, tables, and text.
"""

from diagram_parser import DiagramParser
from math_ocr import MathOCR
from table_extractor import TableExtractor
from image_captioner import ImageCaptioner
from fusion_engine import FusionEngine

class MultimodalReasoning:
    def __init__(self):
        self.diagram_parser = DiagramParser()
        self.math_ocr = MathOCR()
        self.table_extractor = TableExtractor()
        self.image_captioner = ImageCaptioner()
        self.fusion_engine = FusionEngine()

    def process_image(self, image_path):
        diagrams = self.diagram_parser.parse(image_path)
        math_text = self.math_ocr.extract(image_path)
        tables = self.table_extractor.extract(image_path)
        captions = self.image_captioner.caption(image_path)
        return self.fusion_engine.fuse(diagrams, math_text, tables, captions)

if __name__ == "__main__":
    mm = MultimodalReasoning()
    result = mm.process_image("sample.png")
    print(result)
