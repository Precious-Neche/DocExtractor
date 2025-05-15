# DocExtractor
A FastAPI application that extracts text from complex documents (PDF, DOCX, XLSX) and images (PNG, JPG) using OCR (Optical Character Recognition).
![Screenshot (196)](https://github.com/user-attachments/assets/0938d834-f381-49fc-9526-330bf6f44c38)
![Screenshot (197)](https://github.com/user-attachments/assets/88539be8-ce8c-4284-8a9d-c00de05b0725)


## Features

- **Document Processing**  
  - PDF (including password-protected)
  - Word (DOCX)
  - Excel (XLSX)
- **Image OCR**  
  - Text extraction from PNG/JPG using Tesseract
- **Responsive Web UI**  
  - Bootstrap 5 frontend
  - Real-time processing

## Installation

1. Clone the repository
   git clone https://github.com/your-username/document-extractor.git
   cd document-extractor
   
3. Install dependencies
pip install -r requirements.txt

3.Install Tesseract OCR

Windows: Download from UB Mannheim

Mac: brew install tesseract

Linux: sudo apt install tesseract-ocr

4.Run the application
uvicorn app.main:app --reload
5. Open http://localhost:8000
