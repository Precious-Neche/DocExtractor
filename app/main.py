import os
import tempfile
import uuid
from fastapi import FastAPI, Request, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pathlib import Path

from .models import ExtractionResult
from .document_parser import parse_document
from .ocr import extract_text_from_image

app = FastAPI(title="Document Data Extractor")

# Set up templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/extract", response_class=HTMLResponse)
async def extract_data(
    request: Request,
    file: UploadFile,
    password: Optional[str] = Form(None),
):
    temp_file_path = None
    try:
        # Create secure temporary file with UUID
        file_ext = os.path.splitext(file.filename)[1].lower()
        temp_file_name = f"doc_{uuid.uuid4()}{file_ext}"
        temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)
        
        # Write the uploaded file
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process based on file type
        if file_ext in ('.png', '.jpg', '.jpeg'):
            result = extract_text_from_image(temp_file_path)
        else:
            result = parse_document(temp_file_path, password)
        
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "filename": file.filename,
                "content": result.content,
                "metadata": result.metadata
            }
        )
    
    except ValueError as e:
        # Specific handling for password-related errors
        error_detail = str(e)
        if "password" in error_detail.lower():
            error_detail = f"Document password error: {error_detail}"
        raise HTTPException(
            status_code=400,
            detail=error_detail
        )
    
    except Exception as e:
        # Generic error handling
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )
    
    finally:
        # Ensure temp file is always cleaned up
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass  # Silent cleanup if file is already gone

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}