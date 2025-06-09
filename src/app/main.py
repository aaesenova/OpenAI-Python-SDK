from fastapi import FastAPI
from .api.endpoints import jobs
from .database import engine, Base

app = FastAPI(title="AI-Powered Job Description Generator")

# Include routers
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Powered Job Description Generator API"} 