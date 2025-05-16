import pytesseract
from PIL import Image
from typing import Optional, Any

def extract_text_from_image(image_path: str) -> Optional[str]:
    """Extract text from an image using Tesseract OCR."""
    try:
        image: Any = Image.open(image_path)
        text: str = pytesseract.image_to_string(image)
        return text
    except Exception:
        return None

if __name__ == "__main__":
    import os

    # Correct the path to the test image in DesktopAPI/static/img
    image_path = os.path.join(os.path.dirname(__file__), '../static/img/testz_img.png')
    image_path = os.path.abspath(image_path)
    result = extract_text_from_image(image_path)
    print("Extracted Text:", result)
