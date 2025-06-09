from sqlalchemy import create_engine, text
from src.app.models.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Add description column to job_postings if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name='job_postings' 
                AND column_name='description'
            ) THEN 
                ALTER TABLE job_postings 
                ADD COLUMN description TEXT;
            END IF;
        END $$;
        """))
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 