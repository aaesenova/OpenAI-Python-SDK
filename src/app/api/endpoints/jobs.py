from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json
import openai
from ...schemas.schemas import (
    JobPosting,
    JobPostingCreate,
    GenerateDescriptionRequest,
    GenerateDescriptionResponse
)
from ...models.models import JobPosting as JobPostingModel, Company
from ...database import get_db
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_job_description(
    company_name: str,
    company_description: str,
    job_title: str,
    required_tools: List[str]
) -> str:
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional job description writer. Generate a detailed job description based on the provided information."
                },
                {
                    "role": "user",
                    "content": f"""
                    Company: {company_name}
                    Company Description: {company_description}
                    Job Title: {job_title}
                    Required Tools: {', '.join(required_tools)}
                    
                    Please generate a professional job description that includes:
                    1. Brief company introduction
                    2. Role overview
                    3. Key responsibilities
                    4. Required technical skills (focusing on the provided tools)
                    5. Qualifications and experience
                    6. What we offer
                    """
                }
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating description: {str(e)}")

@router.post("/{job_id}/description", response_model=GenerateDescriptionResponse)
async def create_job_description(
    job_id: int,
    request: GenerateDescriptionRequest,
    db: Session = Depends(get_db)
):
    # Get job posting and company information
    job_posting = db.query(JobPostingModel).filter(JobPostingModel.id == job_id).first()
    if not job_posting:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    company = db.query(Company).filter(Company.id == job_posting.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Generate description using OpenAI
    description = generate_job_description(
        company_name=company.name,
        company_description=company.description or "",
        job_title=job_posting.title,
        required_tools=request.required_tools
    )
    
    # Update job posting with new description
    job_posting.description = description
    job_posting.required_tools = json.dumps(request.required_tools)
    db.commit()
    
    return GenerateDescriptionResponse(
        job_id=job_id,
        description=description,
        generated_at=datetime.utcnow()
    ) 