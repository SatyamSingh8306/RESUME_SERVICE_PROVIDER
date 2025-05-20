# Resume Processing Service

This service is responsible for processing and enhancing resumes. It provides APIs for analyzing resumes and optimizing them for specific job positions.

## Features

- Resume text extraction and processing
- Job-specific resume enhancement
- Customizable tone and domain-specific optimization
- JWT-based authentication
- Asynchronous processing with RabbitMQ
- Redis-based caching

## API Endpoints

### Process Resume
- **POST** `/v1/resume/process/{user_id}`
- Process and extract text from a user's resume
- Requires JWT Bearer token in Authorization header

### Enhance Resume
- **POST** `/v1/resume/process/{user_id}?is_job=true`
- Enhance resume for a specific job position
- Requires JWT Bearer token in Authorization header
- Parameters:
  - `job_title`: Target job title
  - `job_description`: Job description
  - `domain`: (Optional) Industry domain
  - `tone`: (Optional) Writing tone (default: "professional")

## Installation

1. Clone the repository

2. Rename the `.env.example` file to `.env` and update the values

```bash
cp .env.example .env
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Run the server

```bash
python -m app
```

## Documentation

After running the server, you can access the documentation at `http://localhost:8000/docs`.
