from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional

class Experience(BaseModel):
    title: str = Field(..., description="Job title or role held")
    company: str = Field(..., description="Company or organization name")
    duration: str = Field(..., description="Time period worked, e.g., Jan 2022 - Dec 2023")
    description: str = Field(..., description="Responsibilities and achievements in this role")

class Education(BaseModel):
    degree: str = Field(..., description="Degree earned, e.g., B.Tech, M.Sc")
    institution: str = Field(..., description="Name of the college/university")
    year: str = Field(..., description="Year of graduation")
    cgpa: Optional[float] = Field(None, description="Optional CGPA or percentage")

class Project(BaseModel):
    title: str = Field(..., description="Project name in clear way")
    tools: List[str] = Field(..., description="List of technologies/tools used")
    description: str = Field(..., description="Short description of the project")

class Certification(BaseModel):
    name: str = Field(..., description="Certificate title")
    issuer: str = Field(..., description="Organization that issued it")
    date: str = Field(None, description="Date of completion or issue")

class Skill(BaseModel):
    name: str = Field(..., description="Skill name")
    level: Literal["Beginner", "Intermediate", "Advanced"] = Field(..., description="Skill proficiency level")

class SocialProfile(BaseModel):
    platform: str = Field(..., description="Platform name (LinkedIn, GitHub, etc.)")
    url: str = Field(..., description="Profile URL")

class Response(BaseModel):
    # Personal Information
    name: str = Field(..., description="Name of the person mentioned")
    graduation: str = Field(..., description="Graduation Degree like Bachelor of Technology")
    specialization: Optional[str] = Field(None, description="Specialization or domain focus")
    experience_level: Literal["Beginner", "Intermediate", "Advanced"] = Field(..., description="Candidate's experience level")
    description: str = Field(..., description="Industry-relevant summary based on interest, skills, and knowledge")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Current city or country")

    # Core CV Sections
    skills: List[Skill] = Field(default_factory=list, description="List of technical and soft skills")
    experiences: List[Experience] = Field(default_factory=list, description="Professional experience details")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    projects: List[Project] = Field(default_factory=list, description="Significant projects")
    certifications: List[Certification] = Field(default_factory=list, description="List of certifications earned")
    social_profiles: List[SocialProfile] = Field(default_factory=list, description="Social and professional links")

    # Optional Sections
    achievements: Optional[List[str]] = Field(None, description="Notable achievements or awards")
    languages: Optional[List[str]] = Field(None, description="Languages known")
    interests: Optional[List[str]] = Field(None, description="Personal or professional interests") 