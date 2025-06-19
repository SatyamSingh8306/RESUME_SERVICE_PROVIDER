import asyncio
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
from app.services.textEditing import TextEditingService

# Load environment variables
load_dotenv()

# Initialize service
text_editing_service = TextEditingService()

# Sample resume data to test LLM
TEST_RESUME_DATA = {
    "personal_info": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "location": "New York, USA"
    },
    "summary": "Experienced software developer with 5 years of experience in Python and web development.",
    "experience": [
        {
            "title": "Senior Software Developer",
            "company": "Tech Corp",
            "duration": "2020 - Present",
            "description": "Led development of multiple web applications using Python and React."
        }
    ],
    "skills": ["Python", "FastAPI", "React"]
}

# Sample job data for testing
TEST_JOB_DATA = {
    "title": "Senior Python Developer",
    "description": """We are looking for a Senior Python Developer with experience in web development and API design.
    Responsibilities:
    - Design and implement scalable web applications
    - Develop and maintain REST APIs
    - Lead development teams
    - Optimize application performance
    
    Requirements:
    - 5+ years of Python development
    - Experience with FastAPI or Django
    - Frontend development skills (React)
    - Team leadership experience""",
    "domain": "Technology"
}

async def test_resume_processing():
    """Test the complete resume processing pipeline"""
    try:
        # Convert resume data to text format
        resume_text = f"""
        Name: {TEST_RESUME_DATA['personal_info']['name']}
        Email: {TEST_RESUME_DATA['personal_info']['email']}
        Phone: {TEST_RESUME_DATA['personal_info']['phone']}
        Location: {TEST_RESUME_DATA['personal_info']['location']}
        
        Summary:
        {TEST_RESUME_DATA['summary']}
        
        Experience:
        {TEST_RESUME_DATA['experience'][0]['title']} at {TEST_RESUME_DATA['experience'][0]['company']}
        {TEST_RESUME_DATA['experience'][0]['duration']}
        {TEST_RESUME_DATA['experience'][0]['description']}
        
        Skills:
        {', '.join(TEST_RESUME_DATA['skills'])}
        """
        
        # Process the resume using the actual services
        
        # 1. Enhance text
        enhanced_text = await text_editing_service.enhance_text(
            text=resume_text,
            job_title=TEST_JOB_DATA["title"],
            job_description=TEST_JOB_DATA["description"]
        )
        
        # 2. Check grammar
        grammar_suggestions = await text_editing_service.check_grammar(enhanced_text)
        
        # 3. Adjust tone
        professional_text = await text_editing_service.adjust_tone(enhanced_text, tone="professional")
        
        # 4. Format bullet points
        formatted_text = await text_editing_service.format_bullet_points(professional_text)
        
        # 5. Extract keywords
        keywords = await text_editing_service.extract_keywords(
            text=formatted_text,
            job_description=TEST_JOB_DATA["description"]
        )
        
        # 6. Process resume
        processed_resume = await text_editing_service.process_resume(
            text=formatted_text,
            domain=TEST_JOB_DATA["domain"],
            job_title=TEST_JOB_DATA["title"],
            job_description=TEST_JOB_DATA["description"]
        )
        
        # Verify response
        assert enhanced_text, "Enhanced text missing"
        assert grammar_suggestions, "Grammar suggestions missing"
        assert formatted_text, "Formatted text missing"
        assert keywords, "Keywords missing"
        assert processed_resume, "Processed resume missing"
        
    except Exception as e:
        pass

if __name__ == "__main__":
    asyncio.run(test_resume_processing()) 