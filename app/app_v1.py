from fastapi import FastAPI

from app.routers import resume  # Only import resume router
from app.utils.errors import (
    BaseException,
    base_exception_handler,
    general_exception_handler,
)

app = FastAPI(
    title="Resume Processing API",
    version="1.0.0",
    description="API for processing and enhancing resumes",
)

# Include only resume router
app.include_router(resume.router)

# Exception handlers
app.add_exception_handler(BaseException, base_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Resume Processing Service",
        "service": "resume",
        "endpoints": {
            "POST /resume/process/{user_id}": "Process or enhance a resume",
        }
    }