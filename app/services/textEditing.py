from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from app.models.responseFormat import Response
from typing import Dict, List, Optional
import re

from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME")

class TextEditingService:
    def __init__(self):
        self.model = self._load_model()

    def _load_model(self, model_name=os.environ.get("MODEL_NAME")):
        model = ChatGroq(
            model=model_name,
            api_key=os.environ.get("GROQ_API_KEY")
        )
        model = model.with_structured_output(Response)
        return model

    def load_resume_content(self, file_path: str) -> str:
        """Load content from PDF resume files"""
        loader = DirectoryLoader(
            path=file_path,
            glob="*.pdf",
            loader_cls=PyMuPDFLoader
        )
        docs = loader.load()
        content = ""
        for i, doc in enumerate(docs):
            content += doc.page_content
        return content

    def process_resume(self, text: str, domain: str, job_title: str, job_description: str) -> Response:
        """Process resume text and return structured data"""
        prompts = PromptTemplate(
            template="""You are an expert HR professional. Your task is to extract information from the given resume text and format it into a structured JSON object matching the following schema:
                    Resume Text:{text}
                    Domain:{domain}
                    Job Title: {job_title}
                    Job Description : {job_description}

                    Instructions:
                    1. Extract relevant information and map it to the appropriate fields in the schema.
                    2. If a field cannot be filled directly from the text, infer its value based on context or leave it blank.
                    3. Make sure that everything is written perfectly in english.
                    4. Add sufficient project according to job title and job description.
                    5. Make it ATS Friendly.
                    6. make sure to return something with validation of it's type so that i don't get error
                    """,
            input_variables=["text", "domain", "job_title", "job_description"],
        )

        chain = prompts | self.model
        result = chain.invoke({
            "text": text,
            "domain": domain,
            "job_title": job_title,
            "job_description": job_description
        })
        return result

    def enhance_text(self, text: str, job_title: str, job_description: str) -> str:
        """Enhance the text to be more professional and ATS-friendly"""
        prompts = PromptTemplate(
            template="""You are an expert resume writer. Enhance the following text to be more professional and ATS-friendly.
            Consider the job title and description while making improvements.
            
            Original Text: {text}
            Job Title: {job_title}
            Job Description: {job_description}
            
            Instructions:
            1. Use strong action verbs
            2. Quantify achievements where possible
            3. Remove any informal language
            4. Ensure proper grammar and punctuation
            5. Make it concise and impactful
            6. Use industry-specific keywords from the job description
            """,
            input_variables=["text", "job_title", "job_description"]
        )
        
        chain = prompts | self.model
        result = chain.invoke({
            "text": text,
            "job_title": job_title,
            "job_description": job_description
        })
        return result

    def check_grammar(self, text: str) -> Dict[str, List[str]]:
        """Check grammar and provide suggestions for improvement"""
        prompts = PromptTemplate(
            template="""You are an expert grammar checker. Analyze the following text and provide grammar suggestions.
            
            Text: {text}
            
            Instructions:
            1. Identify grammar errors
            2. Suggest corrections
            3. Explain why each correction is needed
            4. Format the response as a list of errors and their corrections
            """,
            input_variables=["text"]
        )
        
        chain = prompts | self.model
        result = chain.invoke({"text": text})
        return result

    def adjust_tone(self, text: str, tone: str = "professional") -> str:
        """Adjust the tone of the text to be more professional, confident, or other specified tone"""
        prompts = PromptTemplate(
            template="""You are an expert in professional writing. Adjust the tone of the following text to be more {tone}.
            
            Text: {text}
            Desired Tone: {tone}
            
            Instructions:
            1. Maintain the original meaning
            2. Adjust word choice to match the desired tone
            3. Ensure consistency throughout the text
            4. Keep it concise and clear
            """,
            input_variables=["text", "tone"]
        )
        
        chain = prompts | self.model
        result = chain.invoke({
            "text": text,
            "tone": tone
        })
        return result

    def extract_keywords(self, text: str, job_description: str) -> List[str]:
        """Extract relevant keywords from the text that match the job description"""
        prompts = PromptTemplate(
            template="""You are an expert in resume optimization. Extract relevant keywords from the text that match the job description.
            
            Text: {text}
            Job Description: {job_description}
            
            Instructions:
            1. Identify technical skills
            2. Identify soft skills
            3. Identify industry-specific terms
            4. Prioritize keywords that appear in the job description
            5. Return a list of unique keywords
            """,
            input_variables=["text", "job_description"]
        )
        
        chain = prompts | self.model
        result = chain.invoke({
            "text": text,
            "job_description": job_description
        })
        return result

    def format_bullet_points(self, text: str) -> str:
        """Format text into professional bullet points"""
        prompts = PromptTemplate(
            template="""You are an expert in resume writing. Convert the following text into professional bullet points.
            
            Text: {text}
            
            Instructions:
            1. Start each bullet point with a strong action verb
            2. Keep each point concise (1-2 lines)
            3. Quantify achievements where possible
            4. Ensure consistent formatting
            5. Remove any redundant information
            """,
            input_variables=["text"]
        )
        
        chain = prompts | self.model
        result = chain.invoke({"text": text})
        return result 