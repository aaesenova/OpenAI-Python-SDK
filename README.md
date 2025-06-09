# AI-Powered Job Description Generator

This project is a FastAPI-based application that generates job descriptions using OpenAI's GPT model based on company information and required tools.

## Features

- Generate detailed job descriptions using AI
- Integration with OpenAI's GPT model
- Database storage for job postings and companies
- RESTful API endpoints
- Input validation and error handling

## Prerequisites

- Python 3.8+
- PostgreSQL database
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
OPENAI_API_KEY=your_openai_api_key
```

5. Initialize the database:
```bash
python init.py
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn src.app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Generate Job Description

```http
POST /jobs/{job_id}/description
```

Request body:
```json
{
    "required_tools": ["Python", "TensorFlow", "PyTorch", "AWS"]
}
```

Response:
```json
{
    "job_id": 1,
    "description": "Generated job description...",
    "generated_at": "2024-03-20T10:00:00Z"
}
```

## Error Handling

The API includes comprehensive error handling for:
- Invalid job IDs
- Missing company information
- OpenAI API errors
- Database connection issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 