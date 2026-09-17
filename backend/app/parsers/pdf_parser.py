import pymupdf as fitz  # PyMuPDF
import re
from typing import List, Dict, Any

class PDFParser:
    @staticmethod
    def parse(file_path: str) -> List[Dict[str, Any]]:
        """
        Parses a .pdf file and returns slide/page-by-slide metadata & extracted content.
        """
        doc = fitz.open(file_path)
        slides_data = []

        for index, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            
            # Count images on the page
            image_list = page.get_images(full=True)
            image_count = len(image_list)

            # Bullet detection
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            bullet_count = 0
            for line in lines:
                if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.', 'a.', 'b.')):
                    bullet_count += 1

            word_count = len(re.findall(r'\b\w+\b', text))

            slides_data.append({
                "slide_number": index,
                "raw_text": text,
                "word_count": word_count,
                "bullet_count": bullet_count,
                "image_count": image_count,
            })

        doc.close()
        return slides_data
