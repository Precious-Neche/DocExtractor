# from PIL import Image
# import pytesseract
# from .models import ExtractionResult

# def extract_text_from_image(image_path: str) -> ExtractionResult:
#     try:
#         # Open the image file
#         img = Image.open(image_path)
        
#         # Perform OCR
#         text = pytesseract.image_to_string(img)
        
#         return ExtractionResult(
#             content=text.strip(),
#             metadata={"type": "image", "format": img.format}
#         )
#     except Exception as e:
#         raise ValueError(f"OCR processing error: {str(e)}")

# def extract_text_from_image(image_path: str) -> ExtractionResult:
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img)
        
#         return ExtractionResult(
#             content=text.strip(),  # Must be a string, not an object
#             metadata={
#                 "type": "image",
#                 "format": img.format
#             }
#         )
#     except Exception as e:
#         raise ValueError(f"OCR processing error: {str(e)}")
    
from .models import ExtractionResult
from PIL import Image
import pytesseract

def extract_text_from_image(image_path: str) -> ExtractionResult:
    try:
        # Open image and extract text
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)
        
        # Return PROPERLY structured ExtractionResult
        return ExtractionResult(
            content=extracted_text.strip(),  # MUST be string
            metadata={
                "type": "image",
                "format": img.format,
                "size": img.size
            }
        )
    except Exception as e:
        raise ValueError(f"OCR failed: {str(e)}")