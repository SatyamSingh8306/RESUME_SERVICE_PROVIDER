from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.types.responseFormat import Response
from app.services.system_messages import resume_prompts, enhance_resume_prompts, grammar_resume_prompts, adjust_resume_prompts, extract_keyword_prompts, bullet_format_prompts
from app.utils.pdf_text import fetch_pdf_text
from typing import Dict, List, Optional
from app import (MODEL, GROQ_MODEL, GROQ_API_KEY, USE_GROQ)
import re
import asyncio

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
        content = await fetch_pdf_text(file_url)
        return content

    async def process_resume(self, text: str, domain: str, job_title: str, job_description: str) -> Response:
        """Process resume text and return structured data asynchronously"""
        prompts = PromptTemplate(
            template=resume_prompts,
            input_variables=["text", "domain", "job_title", "job_description"],
        )

        chain = prompts | self.model_structured
        
        result = await asyncio.to_thread(
            chain.invoke,
            {
                "text": text,
                "domain": domain,
                "job_title": job_title,
                "job_description": job_description
            }
        )
        return result

    async def enhance_text(self, text: str, job_title: str, job_description: str) -> str:
        """Enhance the text to be more professional and ATS-friendly asynchronously"""
        prompts = PromptTemplate(
            template=enhance_resume_prompts,
            input_variables=["text", "job_title", "job_description"]
        )
        
        chain = prompts | self.model
        
        result = await asyncio.to_thread(
            chain.invoke,
            {
                "text": text,
                "job_title": job_title,
                "job_description": job_description
            }
        )
        return result.content

    async def check_grammar(self, text: str) -> Dict[str, List[str]]:
        """Check grammar and provide suggestions for improvement asynchronously"""
        prompts = PromptTemplate(
            template=grammar_resume_prompts,
            input_variables=["text"]
        )
        
        chain = prompts | self.model
        
        result = await asyncio.to_thread(
            chain.invoke,
            {"text": text}
        )
        return result.content

    async def adjust_tone(self, text: str, tone: str = "professional") -> str:
        """Adjust the tone of the text to be more professional, confident, or other specified tone asynchronously"""
        prompts = PromptTemplate(
            template=adjust_resume_prompts,
            input_variables=["text", "tone"]
        )
        
        chain = prompts | self.model
        
        result = await asyncio.to_thread(
            chain.invoke,
            {
                "text": text,
                "tone": tone
            }
        )
        return result.content

    async def extract_keywords(self, text: str, job_description: str) -> List[str]:
        """Extract relevant keywords from the text that match the job description asynchronously"""
        prompts = PromptTemplate(
            template=extract_keyword_prompts,
            input_variables=["text", "job_description"]
        )
        
        chain = prompts | self.model
        
        result = await asyncio.to_thread(
            chain.invoke,
            {
                "text": text,
                "job_description": job_description
            }
        )
        return result.content

    async def format_bullet_points(self, text: str) -> str:
        """Format text into professional bullet points asynchronously"""
        prompts = PromptTemplate(
            template=bullet_format_prompts,
            input_variables=["text"]
        )
        
        chain = prompts | self.model
        
        result = await asyncio.to_thread(
            chain.invoke,
            {"text": text}
        )
        return result.content
    