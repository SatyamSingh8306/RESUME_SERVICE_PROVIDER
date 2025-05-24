import asyncio
import logging
from app.services.broker.rpc import RPCService, RPCPayloadType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class LLMResponder:
    """Mock LLM Service Responder"""
    
    @staticmethod
    async def respond_rpc(request_payload: RPCPayloadType) -> dict:
        """Handle LLM requests for resume data"""
        logger.info(f"Received request: {request_payload}")
        
        request_type = request_payload["type"]
        request_data = request_payload["data"]
        
        if request_type == "analyze_resume":
            # Simulate LLM analysis
            return {
                "status": "success",
                "analysis": {
                    "strengths": [
                        "Strong Python development experience",
                        "Good mix of frontend and backend skills",
                        "Proven leadership experience"
                    ],
                    "suggestions": [
                        "Add more specific metrics for achievements",
                        "Include certifications if any",
                        "Expand on project details"
                    ],
                    "overall_score": 85
                }
            }
        elif request_type == "improve_resume":
            # Simulate LLM improvement suggestions
            return {
                "status": "success",
                "improved_sections": {
                    "summary": "Accomplished software developer with 5+ years of experience in full-stack development, specializing in Python and React. Proven track record of leading successful web application projects.",
                    "experience": [
                        {
                            "title": "Senior Software Developer",
                            "company": "Tech Corp",
                            "duration": "2020 - Present",
                            "description": "Led a team of 5 developers in building scalable web applications using Python and React. Improved application performance by 40% and reduced deployment time by 60%."
                        }
                    ]
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Unknown request type: {request_type}"
            }

async def test_llm_resume():
    """Test LLM responses with resume data"""
    try:
        # Start the LLM service responder
        responder_task = asyncio.create_task(RPCService.respond(LLMResponder()))
        
        # Wait for the service to start
        await asyncio.sleep(2)
        
        # Test 1: Analyze Resume
        logger.info("Testing: Analyze Resume")
        analyze_payload = RPCService.build_request_payload(
            type="analyze_resume",
            data=TEST_RESUME_DATA
        )
        
        analyze_response = await RPCService.request(
            service_rpc="llm_service",
            request_payload=analyze_payload,
            timeout=5
        )
        logger.info(f"Analysis Response: {analyve_response}")
        
        # Test 2: Improve Resume
        logger.info("Testing: Improve Resume")
        improve_payload = RPCService.build_request_payload(
            type="improve_resume",
            data=TEST_RESUME_DATA
        )
        
        improve_response = await RPCService.request(
            service_rpc="llm_service",
            request_payload=improve_payload,
            timeout=5
        )
        logger.info(f"Improvement Response: {improve_response}")
        
        # Verify responses
        assert analyze_response["status"] == "success"
        assert improve_response["status"] == "success"
        assert "analysis" in analyze_response
        assert "improved_sections" in improve_response
        
        logger.info("All LLM tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
    finally:
        # Clean up
        responder_task.cancel()
        try:
            await responder_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(test_llm_resume()) 