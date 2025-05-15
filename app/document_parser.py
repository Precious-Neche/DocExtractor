from pypdf import PdfReader
from docx import Document
import openpyxl
from typing import Optional
from .models import ExtractionResult
import io
import magic

def parse_document(file_path: str, password: Optional[str] = None) -> ExtractionResult:
    if file_path.endswith('.pdf'):
        return parse_pdf(file_path, password)
    elif file_path.endswith('.docx'):
        return parse_docx(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return parse_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

def parse_pdf(file_path: str, password: Optional[str]) -> ExtractionResult:
    content = ""
    metadata = {"type": "pdf", "pages": 0}
    
    try:
        reader = PdfReader(file_path)
        if reader.is_encrypted:
            if password:
                reader.decrypt(password)
            else:
                raise ValueError("PDF is password protected but no password provided")
        
        metadata["pages"] = len(reader.pages)
        for page in reader.pages:
            content += page.extract_text() + "\n\n"
            
    except Exception as e:
        raise ValueError(f"PDF processing error: {str(e)}")
    
    return ExtractionResult(content=content.strip(), metadata=metadata)

def parse_docx(file_path: str) -> ExtractionResult:
    content = ""
    metadata = {"type": "docx"}
    
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            content += para.text + "\n"
    except Exception as e:
        raise ValueError(f"DOCX processing error: {str(e)}")
    
    return ExtractionResult(content=content.strip(), metadata=metadata)

def parse_excel(file_path: str) -> ExtractionResult:
    content = []
    metadata = {"type": "excel", "sheets": 0}
    
    try:
        wb = openpyxl.load_workbook(file_path)
        metadata["sheets"] = len(wb.sheetnames)
        
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            content.append(f"\n--- Sheet: {sheet_name} ---\n")
            
            for row in sheet.iter_rows(values_only=True):
                row_content = " | ".join(str(cell) if cell is not None else "" for cell in row)
                content.append(row_content)
    except Exception as e:
        raise ValueError(f"Excel processing error: {str(e)}")
    
    return ExtractionResult(content="\n".join(content), metadata=metadata)