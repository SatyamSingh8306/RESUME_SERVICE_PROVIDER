from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from pydantic import BaseModel
import json
from app.services.textEditing import loader, chaining
import tempfile
import os

router = APIRouter(prefix="/resume", tags=["resume"])

class ResumeRequest(BaseModel):
    domain: str
    job_title: str
    job_description: str
    resume_text: Optional[str] = None

@router.post("/process")
async def process_resume(
    file: Optional[UploadFile] = File(None),
    domain: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    resume_text: Optional[str] = Form(None)
):
    try:
        content = ""
        
        # Handle file upload if provided
        if file:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are supported")
            
            # Create a temporary directory for the PDF
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, file.filename)
                
                # Save the uploaded file
                with open(temp_file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                
                # Process the PDF
                content = loader(temp_dir)
        
        # Use provided text if no file was uploaded
        elif resume_text:
            content = resume_text
        else:
            raise HTTPException(status_code=400, detail="Either a PDF file or resume text must be provided")

        # Process the resume using the existing chaining function
        result = chaining(
            text=content,
            domain=domain,
            job_title=job_title,
            job_description=job_description
        )

        # Convert the Response model to JSON
        return result.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 