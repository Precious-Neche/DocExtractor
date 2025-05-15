import os
import magic
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
    try:
        # Save the uploaded file temporarily
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Determine file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        # Process the file based on its type
        if "image" in file_type:
            # THIS IS THE CRITICAL FIX - use the result directly
            result = extract_text_from_image(file_path)
        else:
            result = parse_document(file_path, password)
        
        # Clean up
        os.remove(file_path)
        
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "filename": file.filename,
                "content": result.content,  # Already a string
                "metadata": result.metadata  # Already a dict
            }
        )
    
    except Exception as e:
        # Clean up temp file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))