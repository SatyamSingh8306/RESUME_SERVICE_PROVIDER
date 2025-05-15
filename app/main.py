from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging
from app.services.orchestrator import ResumeOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resume Builder API",
    version="0.1.0",
)

# Initialize orchestrator
orchestrator = ResumeOrchestrator()

class ResumeRequest(BaseModel):
    user_data: Dict[str, Any]

@app.post("/api/build-resume")
async def build_resume(request: ResumeRequest):
    try:
        logger.info("Received resume build request")
        result = await orchestrator.process_resume(request.user_data)
        logger.info("Resume built successfully")
        return result
    except Exception as e:
        logger.error(f"Error building resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resume/{user_id}")
async def get_resume(user_id: str):
    try:
        logger.info(f"Fetching resume for user: {user_id}")
        result = await orchestrator.get_resume(user_id)
        logger.info(f"Resume retrieved successfully for user: {user_id}")
        return result
    except Exception as e:
        logger.error(f"Error retrieving resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to Resume Builder API"}
