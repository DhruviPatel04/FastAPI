from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

class material(BaseModel):
    title: str
    description: str
    file_URL: str
    module_id: int
 