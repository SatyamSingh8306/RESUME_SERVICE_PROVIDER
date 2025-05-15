from typing import Dict, Any
import logging
from app.services.aws import AWSService
from app.services.redis import RedisService
from app.services.textEditing import TextEditingService
from app.services.azure import AzureService

logger = logging.getLogger(__name__)

class ResumeOrchestrator:
    def __init__(self):
        self.aws_service = AWSService()
        self.redis_service = RedisService()
        self.text_editing_service = TextEditingService()
        self.azure_service = AzureService()

    async def process_resume(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Step 1: Store user data in Redis for caching
            await self.redis_service.store_user_data(user_data)

            # Step 2: Process text using Azure services
            processed_text = await self.azure_service.process_text(user_data.get("content", ""))

            # Step 3: Apply text editing and formatting using TextEditingService
            # First enhance the text
            enhanced_text = self.text_editing_service.enhance_text(
                text=processed_text,
                job_title=user_data.get("job_title", ""),
                job_description=user_data.get("job_description", "")
            )

            # Check grammar
            grammar_suggestions = self.text_editing_service.check_grammar(enhanced_text)

            # Adjust tone to be professional
            professional_text = self.text_editing_service.adjust_tone(enhanced_text, tone="professional")

            # Format into bullet points
            formatted_text = self.text_editing_service.format_bullet_points(professional_text)

            # Extract keywords for ATS optimization
            keywords = self.text_editing_service.extract_keywords(
                text=formatted_text,
                job_description=user_data.get("job_description", "")
            )

            # Step 4: Process the resume with domain-specific information
            processed_resume = self.text_editing_service.process_resume(
                text=formatted_text,
                domain=user_data.get("domain", ""),
                job_title=user_data.get("job_title", ""),
                job_description=user_data.get("job_description", "")
            )

            # Step 5: Generate PDF using AWS services
            pdf_url = await self.aws_service.generate_pdf(processed_resume)

            # Step 6: Store the final resume in Redis
            final_resume = {
                "user_data": user_data,
                "processed_resume": processed_resume,
                "formatted_text": formatted_text,
                "grammar_suggestions": grammar_suggestions,
                "keywords": keywords,
                "pdf_url": pdf_url
            }
            await self.redis_service.store_resume(final_resume)

            return {
                "status": "success",
                "message": "Resume processed successfully",
                "data": final_resume
            }

        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            raise Exception(f"Failed to process resume: {str(e)}")

    async def get_resume(self, user_id: str) -> Dict[str, Any]:
        try:
            # Try to get from Redis cache first
            cached_resume = await self.redis_service.get_resume(user_id)
            if cached_resume:
                return cached_resume

            # If not in cache, get from AWS
            resume_data = await self.aws_service.get_resume(user_id)
            if resume_data:
                # Cache the result
                await self.redis_service.store_resume(resume_data)
                return resume_data

            raise Exception("Resume not found")

        except Exception as e:
            logger.error(f"Error retrieving resume: {str(e)}")
            raise Exception(f"Failed to retrieve resume: {str(e)}") 