# Resume Builder API

This service is responsible for building professional resumes based on user input. It provides a simple API endpoint to generate well-formatted resumes in various formats.

## Features

- Resume building from user data
- JSON response format
- Easy to integrate API

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app.main:app --reload
```

## API Usage

### Build Resume
POST `/api/build-resume`

Request body:
```json
{
    "user_data": {
        "name": "John Doe",
        "experience": [...],
        "education": [...],
        "skills": [...]
    }
}
```

Response:
```json
{
    "status": "success",
    "message": "Resume built successfully",
    "resume_data": {...}
}
```

## Development

The project uses FastAPI for the backend API. The main functionality is in `app/main.py`.
