from typing import Dict, Any, List, Optional
import logging
from app.services.broker.rpc import RPCService, RPCPayloadType
from app.services.redis import RedisService
from app.services.textEditing import TextEditingService

logger = logging.getLogger(__name__)

class ResumeProcessor:
    """
    Complete service for fetching, parsing and enhancing resumes
    Integrates RPC, LangChain parsing, Redis caching, and TextEditingService
    """
    
    def __init__(self):
        self.redis_service = RedisService()
        self.text_editing_service = TextEditingService()
    
    async def get_resume_url(self, user_id: str) -> str:
        """
        Fetch the resume URL for a given user ID using RPC service
        
        Args:
            user_id: The user ID to fetch the resume for
            
        Returns:
            The URL to the user's resume PDF
        """
        try:
            response = await RPCService.request(
                "USER_RPC",
                RPCService.build_request_payload(
                    type=RPCPayloadType.GET_USER_RESUME,
                    data={"userId": user_id},
                ),
            )
            
            if not response or "data" not in response or "url" not in response["data"]:
                raise ValueError(f"Invalid response format or missing URL for user {user_id}")
                
            return response["data"]
        
        except Exception as e:
            logger.error(f"Error fetching resume URL for user {user_id}: {str(e)}")
            raise Exception(f"Failed to fetch resume URL: {str(e)}")
    
    async def get_resume_text(self, user_id: str) -> str:
        """
        Get the raw text content of a resume
        
        Args:
            user_id: The user ID to fetch the resume for
            
        Returns:
            Raw text content of the resume
        """
        try:
            
            cached_text = await self.redis_service.get_resume_raw_text(user_id)
            if cached_text:
                logger.info(f"Retrieved resume text from cache for user {user_id}")
                return cached_text
            
            resume_url = await self.get_resume_url(user_id)
            
            resume_text = await self.text_editing_service.load_resume_content(resume_url)
            
            await self.redis_service.store_resume_raw_text(user_id, resume_text)
            
            return resume_text
            
        except Exception as e:
            logger.error(f"Error getting resume text for user {user_id}: {str(e)}")
            raise Exception(f"Failed to get resume text: {str(e)}")
    
    async def enhance_resume(
        self, 
        user_id: str, 
        job_title: str, 
        job_description: str,
        domain: str = "",
        user_data : str= "",
        tone: str = "professional"
    ) -> Dict[str, Any]:
        """
        Process and enhance a resume for a specific job
        
        Args:
            user_id: The user ID to fetch and enhance the resume for
            job_title: The title of the job being applied for
            job_description: The description of the job being applied for
            domain: The domain/industry of the job
            tone: The tone to adjust the resume to
            
        Returns:
            Dictionary with the enhanced resume and related data
        """
        try:
            resume_text = await self.get_resume_text(user_id)
            
            enhanced_text = await self.text_editing_service.enhance_text(
                text=resume_text,
                job_title=job_title,
                job_description=job_description
            )
            
            grammar_suggestions = await self.text_editing_service.check_grammar(enhanced_text)
            
            professional_text = await self.text_editing_service.adjust_tone(enhanced_text, tone=tone)
            
            formatted_text = await self.text_editing_service.format_bullet_points(professional_text)
            
            keywords = await self.text_editing_service.extract_keywords(
                text=formatted_text,
                job_description=job_description
            )
            
            processed_resume = await self.text_editing_service.process_resume(
                text=formatted_text,
                domain=domain,
                job_title=job_title,
                job_description=job_description
            )
            
            result = {
                "user_id": user_id,
                "original_text": resume_text,
                "enhanced_text": enhanced_text,
                "formatted_text": formatted_text,
                "grammar_suggestions": grammar_suggestions,
                "keywords": keywords,
                "processed_resume": processed_resume
            }
            
            await self.redis_service.store_enhanced_resume(user_id, job_title, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error enhancing resume for user {user_id}: {str(e)}")
            return {
                "status": "error",
                "user_id": user_id,
                "error": str(e)
            }
    
    async def get_enhanced_resume(
        self, 
        user_id: str, 
        job_title: str
    ) -> Dict[str, Any]:
        """
        Retrieve a previously enhanced resume
        
        Args:
            user_id: The user ID to retrieve the resume for
            job_title: The job title the resume was enhanced for
            
        Returns:
            The enhanced resume data if found
        """
        try:
            cached_resume = await self.redis_service.get_enhanced_resume(user_id, job_title)
            if cached_resume:
                return cached_resume
                
            raise Exception(f"Enhanced resume not found for user {user_id} and job {job_title}")
            
        except Exception as e:
            logger.error(f"Error retrieving enhanced resume: {str(e)}")
            return {
                "status": "error",
                "user_id": user_id,
                "job_title": job_title,
                "error": str(e)
            }