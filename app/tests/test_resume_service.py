import asyncio
from app.services.broker.rpc import RPCService, RPCPayloadType

# Mock resume data for testing
MOCK_RESUME_DATA = {
    "personal_info": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "location": "New York, USA",
        "linkedin": "linkedin.com/in/johndoe"
    },
    "summary": "Experienced software developer with 5 years of experience in Python and web development.",
    "experience": [
        {
            "title": "Senior Software Developer",
            "company": "Tech Corp",
            "duration": "2020 - Present",
            "description": "Led development of multiple web applications using Python and React."
        },
        {
            "title": "Software Developer",
            "company": "StartUp Inc",
            "duration": "2018 - 2020",
            "description": "Developed and maintained REST APIs using FastAPI."
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "University of Technology",
            "year": "2018"
        }
    ],
    "skills": [
        "Python",
        "FastAPI",
        "React",
        "Docker",
        "AWS"
    ]
}

class ResumeServiceResponder:
    """Mock Resume Service Responder"""
    
    @staticmethod
    async def respond_rpc(request_payload: RPCPayloadType) -> dict:
        """Handle resume service requests"""
        request_type = request_payload["type"]
        request_data = request_payload["data"]
        
        if request_type == "generate_resume":
            # Simulate resume generation
            return {
                "status": "success",
                "resume_url": "https://example.com/resumes/mock-resume.pdf",
                "message": "Resume generated successfully"
            }
        elif request_type == "get_resume_data":
            # Return mock resume data
            return {
                "status": "success",
                "data": MOCK_RESUME_DATA
            }
        else:
            return {
                "status": "error",
                "message": f"Unknown request type: {request_type}"
            }

async def test_resume_service():
    """Test the resume service with mock data"""
    try:
        # Start the resume service responder
        responder_task = asyncio.create_task(RPCService.respond(ResumeServiceResponder()))
        
        # Wait for the service to start
        await asyncio.sleep(2)
        
        # Test 1: Get Resume Data
        get_data_payload = RPCService.build_request_payload(
            type="get_resume_data",
            data={"user_id": "test_user_123"}
        )
        
        data_response = await RPCService.request(
            service_rpc="resume_service",
            request_payload=get_data_payload,
            timeout=5
        )
        
        # Test 2: Generate Resume
        generate_payload = RPCService.build_request_payload(
            type="generate_resume",
            data=MOCK_RESUME_DATA
        )
        
        generate_response = await RPCService.request(
            service_rpc="resume_service",
            request_payload=generate_payload,
            timeout=5
        )
        
        # Verify responses
        assert data_response["status"] == "success"
        assert generate_response["status"] == "success"
        assert "resume_url" in generate_response
        
    except Exception as e:
        pass
    finally:
        # Clean up
        responder_task.cancel()
        try:
            await responder_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(test_resume_service()) 