from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    description: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JobPostingBase(BaseModel):
    title: str
    company_id: int
    location: Optional[str] = None
    description: Optional[str] = None
    required_tools: Optional[List[str]] = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GenerateDescriptionRequest(BaseModel):
    required_tools: List[str] = Field(..., description="List of required tools for the job")

class GenerateDescriptionResponse(BaseModel):
    job_id: int
    description: str
    generated_at: datetime 