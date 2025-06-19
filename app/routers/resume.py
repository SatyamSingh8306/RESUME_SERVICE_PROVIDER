from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Annotated, Dict, Any

from app.dependencies import authorize
from app.utils.resume_url import get_resume_url
from app.services.resume_processor import ResumeProcessor
from app.types.responseFormat import UserData

router = APIRouter(prefix="/resume", tags=["resume"])

class JobDetails(BaseModel):
    job_title: str
    job_description: str
    domain: Optional[str] = ""
    tone: Optional[str] = "professional"

@router.post("/process/{user_id}")
async def process_resume(
        user_id: Annotated[str, Depends(authorize)],
        job_details: JobDetails = None,
        is_job: bool = False,
        user_data : str = " "
) -> Dict[str, Any]:
    try:
        resume_processor = ResumeProcessor()
        
        if is_job and job_details:
            result = await resume_processor.enhance_resume(
                user_id=user_id,
                user_data = user_data,
                job_title=job_details.job_title,
                job_description=job_details.job_description,
                domain=job_details.domain,
                tone=job_details.tone
            )
            return result
        else:
            resume_text = await resume_processor.get_resume_text(user_id)
            return {"user_id": user_id, "resume_text": resume_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create/{user_id}")
async def create_resume(
        user_id: Annotated[str, Depends(authorize)],
        user_data: UserData
) -> Dict[str, Any]:
    try:
        resume_processor = ResumeProcessor()
        result = await resume_processor.create_resume_from_user_data(
            user_id=user_id,
            user_data=user_data.model_dump()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))