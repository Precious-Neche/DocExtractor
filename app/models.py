from pydantic import BaseModel
from typing import Dict, Any

class ExtractionResult(BaseModel):
    content: str  
    metadata: Dict[str, Any] = {}  