from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.types.responseFormat import Response
from app.services.system_messages import resume_prompts, enhance_resume_prompts, grammar_resume_prompts, adjust_resume_prompts, extract_keyword_prompts, bullet_format_prompts, user_data_resume_prompt
from app.utils.pdf_text import fetch_pdf_text
from typing import Dict, List, Optional
from app import (MODEL, GROQ_MODEL, GROQ_API_KEY, USE_GROQ)
import re
import asyncio
from app.utils.errors.exceptions import PDFTextExtractionError, LLMServiceError

class TextEditingService:
    def __init__(self):
        self.model_structured = self._load_model()
        self.model = self._load_llm()

    def _load_llm(self):
        model = ChatGroq(
            model=GROQ_MODEL,
            api_key=GROQ_API_KEY
        ) if USE_GROQ else ChatOllama(model=MODEL)

        parser = StrOutputParser()
        chain = model | parser
        return chain
    
    def _load_model(self):
        model = ChatGroq(
            model=GROQ_MODEL,
            api_key=GROQ_API_KEY
        ) if USE_GROQ else ChatOllama(model=MODEL)
        model = model.with_structured_output(Response)
        return model

    async def load_resume_content(self, file_url: str) -> str:
        """Load content from PDF resume files asynchronously"""
        try:
            content = await fetch_pdf_text(file_url)
            if not content:
                raise PDFTextExtractionError()
            return content
        except Exception as e:
            raise PDFTextExtractionError(str(e))

    async def process_resume(self, text: str, domain: str, job_title: str, job_description: str, user_data: str) -> Response:
        """Process resume text and return structured data asynchronously"""
        prompts = PromptTemplate(
            template=resume_prompts,
            input_variables=["text", "domain", "job_title", "job_description","user_data"],
        )
        chain = prompts | self.model_structured
        try:
            result = await asyncio.to_thread(
                chain.invoke,
                {
                    "text": text,
                    "domain": domain,
                    "job_title": job_title,
                    "job_description": job_description,
                    "user_data" : user_data
                }
            )
            return result
        except Exception as e:
            raise LLMServiceError(str(e))

    async def enhance_text(self, text: str, job_title: str, job_description: str) -> str:
        """Enhance the text to be more professional and ATS-friendly asynchronously"""
        prompts = PromptTemplate(
            template=enhance_resume_prompts,
            input_variables=["text", "job_title", "job_description"]
        )
        chain = prompts | self.model
        try:
            result = await asyncio.to_thread(
                chain.invoke,
                {
                    "text": text,
                    "job_title": job_title,
                    "job_description": job_description
                }
            )
            return result
        except Exception as e:
            raise LLMServiceError(str(e))

    async def check_grammar(self, text: str) -> Dict[str, List[str]]:
        """Check grammar and provide suggestions for improvement asynchronously"""
        prompts = PromptTemplate(
            template=grammar_resume_prompts,
            input_variables=["text"]
        )
        chain = prompts | self.model
        try:
            result = await asyncio.to_thread(
                chain.invoke,
                {"text": text}
            )
            return result
        except Exception as e:
            raise LLMServiceError(str(e))

    async def adjust_tone(self, text: str, tone: str = "professional") -> str:
        """Adjust the tone of the text to be more professional, confident, or other specified tone asynchronously"""
        prompts = PromptTemplate(
            template=adjust_resume_prompts,
            input_variables=["text", "tone"]
        )
        chain = prompts | self.model
        try:
            result = await asyncio.to_thread(
                chain.invoke,
                {
                    "text": text,
                    "tone": tone
                }
            )
            return result
        except Exception as e:
            raise LLMServiceError(str(e))

    async def extract_keywords(self, text: str, job_description: str) -> List[str]:
        """Extract relevant keywords from the text that match the job description asynchronously"""
        prompts = PromptTemplate(
            template=extract_keyword_prompts,
            input_variables=["text", "job_description"]
        )
        chain = prompts | self.model
        try:
            result = await asyncio.to_thread(
                chain.invoke,
                {
                    "text": text,
                    "job_description": job_description
                }
            )
            return result
        except Exception as e:
            raise LLMServiceError(str(e))

    async def format_bullet_points(self, text: str) -> str:
        """Format text into professional bullet points asynchronously"""
        prompts = PromptTemplate(
            template=bullet_format_prompts,
            input_variables=["text"]
        )
        chain = prompts | self.model
        try:
            result = await asyncio.to_thread(
                chain.invoke,
                {"text": text}
            )
            return result
        except Exception as e:
            raise LLMServiceError(str(e))

    async def create_resume_from_user_data(self, user_data: dict) -> str:
        """Create a resume from user data using a custom prompt asynchronously."""
        prompts = PromptTemplate(
            template=user_data_resume_prompt,
            input_variables=["user_data"]
        )
        chain = prompts | self.model
        try:
            result = await asyncio.to_thread(
                chain.invoke,
                {"user_data": str(user_data)}
            )
            return result
        except Exception as e:
            raise LLMServiceError(str(e))
    