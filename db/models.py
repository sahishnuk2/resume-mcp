from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from dotenv import load_dotenv
from datetime import date, datetime, timezone
import os

load_dotenv()

POSTGRESQL_URL = os.getenv("POSTGRESQL_URL")

if not POSTGRESQL_URL:
    raise ValueError("POSTGRESQL_URL not found in .env")

engine = create_engine(POSTGRESQL_URL)

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    description: str = Field()
    tech_stack: str = Field(max_length=200)
    link: str | None = Field(default=None, max_length=200)
    start_date: date = Field()
    end_date: date | None = Field(default=None)

class Work(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    company: str = Field(max_length=100)
    role: str = Field(max_length=100)
    description: str = Field()
    start_date: date = Field()
    end_date: date | None = Field(default=None)

class Skill(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    category: str = Field(max_length=100)
    

class Education(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    institution: str = Field(max_length=100)
    degree: str = Field(max_length=100)
    field: str = Field(max_length=100)
    minor: str | None = Field(default=None, max_length=100)
    end_date: date

class EducationAchievement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    education_id: int = Field(foreign_key="education.id")
    achievement: str = Field(max_length=200)

class RelevantCourse(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    education_id: int = Field(foreign_key="education.id")
    course_name: str = Field(max_length=100)
    grade: str = Field(max_length=5)

class SavedResume(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    version_name: str = Field(max_length=100)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session