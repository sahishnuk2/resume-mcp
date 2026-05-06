import os
import subprocess

from fastmcp import FastMCP
from pydantic import BaseModel
from services.resume_service import (
    add_project, delete_project, get_all_data, get_resume, update_project,
    add_work, delete_work, update_work,
    add_skill, delete_skill, update_skill,
    update_education,
    add_education_achievement, delete_education_achievement, update_education_achievement,
    add_relevant_course, delete_relevant_course, update_relevant_course,
    add_saved_resume, delete_saved_resume, update_saved_resume,
    update_personal
)

mcp = FastMCP("Resume-MCP-Server")

class ProjectInput(BaseModel):
    name: str
    description: str
    tech_stack: str
    link: str | None = None
    start_date: str # format: "Mon YYYY" e.g. "Sep 2025"
    end_date: str | None = None # format: "Mon YYYY" e.g. "Sep 2025"

class ProjectUpdate(BaseModel):
    name: str                          # required to find the project
    description: str | None = None     # only pass if updating
    tech_stack: str | None = None
    link: str | None = None
    start_date: str | None = None # format: "Mon YYYY" e.g. "Sep 2025"
    end_date: str | None = None # format: "Mon YYYY" e.g. "Sep 2025"

class WorkInput(BaseModel):
    company: str
    role: str
    description: str
    start_date: str # format: "Mon YYYY" e.g. "Sep 2025"
    end_date: str | None = None # format: "Mon YYYY" e.g. "Sep 2025"

class WorkUpdate(BaseModel):
    company: str
    role: str | None = None
    description: str | None = None
    start_date: str # format: "Mon YYYY" e.g. "Sep 2025"
    end_date: str | None = None # format: "Mon YYYY" e.g. "Sep 2025"

@mcp.tool()
def modify_project(action: str, project: ProjectInput | None = None, update: ProjectUpdate | None = None) -> str:
    """
    Modify a project entry in the resume database.

    Actions:
    - "add": Add a new project. Requires 'project' with name, description, tech_stack, start_date. Optional: link, end_date.
    - "update": Update an existing project. Requires 'update' with name to identify project. Only pass fields to change.
    - "delete": Delete a project. Requires 'project' with name only.

    Dates must be in format "Mon YYYY" e.g. "Sep 2025"
    """
    try:
        if action == "add":
            add_project(**project.model_dump())
        elif action == "delete":
            delete_project(project.name)
        elif action == "update":
            update_project(**update.model_dump())
        else:
            return "Action must be 'add', 'delete' or 'update' only"
        return "Project tables updated"
    except Exception as e:
        return "Error: " + str(e)
    
@mcp.tool()
def modify_work(action: str, work: WorkInput | None = None, update: WorkUpdate | None = None) -> str:
    """
    Modify a work experience entry in the resume database.

    Actions:
    - "add": Add a new work experience. Requires 'work' with company, role, description, start_date. Optional: end_date.
    - "update": Update an existing work experience. Requires 'update' with company to identify work experience. Only pass fields to change.
    - "delete": Delete a work experience. Requires 'work' with company only.

    Dates must be in format "Mon YYYY" e.g. "Sep 2025"
    """
    try:
        if action == "add":
            add_work(**work.model_dump())
        elif action == "delete":
            delete_work(work.company)
        elif action == "update":
            update_work(**update.model_dump())
        else:
            return "Action must be 'add', 'delete' or 'update' only"
        return "Work tables updated"
    except Exception as e:
        return "Error: " + str(e)

class SkillInput(BaseModel):
    name: str
    category: str

class SkillUpdate(BaseModel):
    name: str               # required to find the skill
    category: str | None = None

@mcp.tool()
def modify_skill(action: str, skill: SkillInput | None = None, update: SkillUpdate | None = None) -> str:
    """
    Modify a skill entry in the resume database.

    Actions:
    - "add": Add a new skill. Requires 'skill' with name and category.
    - "update": Update an existing skill. Requires 'update' with name to identify skill. Only pass fields to change.
    - "delete": Delete a skill. Requires 'skill' with name only.
    """
    try:
        if action == "add":
            add_skill(**skill.model_dump())
        elif action == "delete":
            delete_skill(skill.name)
        elif action == "update":
            update_skill(**update.model_dump())
        else:
            return "Action must be 'add', 'delete' or 'update' only"
        return "Skill tables updated"
    except Exception as e:
        return "Error: " + str(e)

class EducationUpdate(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field: str | None = None
    minor: str | None = None
    end_date: str | None = None # format: "Mon YYYY" e.g. "Sep 2025"

@mcp.tool()
def modify_education(update: EducationUpdate) -> str:
    """
    Update the single education entry in the resume database.
    Only pass fields to change. Dates must be in format "Mon YYYY" e.g. "Sep 2025"
    """
    try:
        update_education(**update.model_dump())
        return "Education table updated"
    except Exception as e:
        return "Error: " + str(e)

class EducationAchievementInput(BaseModel):
    achievement: str

class EducationAchievementUpdate(BaseModel):
    achievement: str            # required to find the achievement
    new_achievement: str        # required replacement text

@mcp.tool()
def modify_education_achievement(action: str, achievement: EducationAchievementInput | None = None, update: EducationAchievementUpdate | None = None) -> str:
    """
    Modify an education achievement entry in the resume database.

    Actions:
    - "add": Add a new achievement. Requires 'achievement' with achievement text.
    - "update": Update an existing achievement. Requires 'update' with achievement to identify and new_achievement as replacement.
    - "delete": Delete an achievement. Requires 'achievement' with achievement text.
    """
    try:
        if action == "add":
            add_education_achievement(achievement.achievement)
        elif action == "delete":
            delete_education_achievement(achievement.achievement)
        elif action == "update":
            update_education_achievement(**update.model_dump())
        else:
            return "Action must be 'add', 'delete' or 'update' only"
        return "Education achievement tables updated"
    except Exception as e:
        return "Error: " + str(e)

class RelevantCourseInput(BaseModel):
    course_name: str
    grade: str

class RelevantCourseUpdate(BaseModel):
    course_name: str                    # required to find the course
    grade: str | None = None

@mcp.tool()
def modify_relevant_course(action: str, course: RelevantCourseInput | None = None, update: RelevantCourseUpdate | None = None) -> str:
    """
    Modify a relevant course entry in the resume database.

    Actions:
    - "add": Add a new course. Requires 'course' with course_name and grade.
    - "update": Update an existing course. Requires 'update' with course_name to identify course. Only pass fields to change.
    - "delete": Delete a course. Requires 'course' with course_name only.
    """
    try:
        if action == "add":
            add_relevant_course(**course.model_dump())
        elif action == "delete":
            delete_relevant_course(course.course_name)
        elif action == "update":
            update_relevant_course(**update.model_dump())
        else:
            return "Action must be 'add', 'delete' or 'update' only"
        return "Relevant course tables updated"
    except Exception as e:
        return "Error: " + str(e)

class SavedResumeInput(BaseModel):
    version_name: str
    content: str

class SavedResumeUpdate(BaseModel):
    version_name: str           # required to find the resume
    content: str | None = None  # only pass if updating

@mcp.tool()
def modify_saved_resume(action: str, resume: SavedResumeInput | None = None, update: SavedResumeUpdate | None = None) -> str:
    """
    Modify a saved resume entry in the resume database.

    Actions:
    - "add": Add a new saved resume. Requires 'resume' with version_name and content.
    - "update": Update an existing saved resume. Requires 'update' with version_name to identify resume. Only pass fields to change.
    - "delete": Delete a saved resume. Requires 'resume' with version_name only.
    """
    try:
        if action == "add":
            add_saved_resume(**resume.model_dump())
        elif action == "delete":
            delete_saved_resume(resume.version_name)
        elif action == "update":
            update_saved_resume(**update.model_dump())
        else:
            return "Action must be 'add', 'delete' or 'update' only"
        return "Saved resume tables updated"
    except Exception as e:
        return "Error: " + str(e)
    
class PersonalInfoUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    github: str | None = None
    linkedin: str | None = None

@mcp.tool()
def modify_personal_info(update: PersonalInfoUpdate) -> str:
    """
    Update the single personal info entry in the resume database.
    Only pass fields to change.
    """
    try:
        update_personal(**update.model_dump())
        return "Personal info updated"
    except Exception as e:
        return "Error: " + str(e)

@mcp.resource("resume://data")
def get_resume_data():
    try:
        return get_all_data()
    except Exception as e:
        return "Error: " + str(e)
    
@mcp.tool()
def compile_resume(version_name: str):
    """Compile a saved LaTeX resume to PDF given the version name."""
    try:
        content = get_resume(version_name)
        output_dir = f"/Users/sahishnukumaar/Desktop/NUS-Study-Materials/Resume/{version_name}"
        os.makedirs(output_dir, exist_ok=True)
        
        tex_path = f"{output_dir}/{version_name}.tex"
        with open(tex_path, "w") as f:
            f.write(content)
        
        subprocess.run(["pdflatex", "-output-directory", output_dir, tex_path])
        return f"PDF saved to {output_dir}/{version_name}.pdf"
    except Exception as e:
        return "Error: " + str(e)

@mcp.prompt()
def generate_resume_prompt(job_description: str) -> str:
    return f"""
    You are a professional resume writer.
    
    Follow these steps:
    1. Read all resume data using the resume://data resource
    2. Analyse this job description:
    {job_description}
    3. Select the most relevant projects and work experiences for this role
    4. Rewrite bullet points with impact and metrics
    5. Do NOT fabricate or exaggerate metrics — only use real information from the resume data
    6. Keep the resume to one page worth of content
    7. Format the final resume as a complete compilable LaTeX document with:
        - Use article documentclass with 11pt font
        - Margins: 0.5in all sides
        - Sections in order: Personal Info, Education, Skills, Projects, Work Experience
        - Use itemize for bullet points
        - Bold company/project names
        - Right align dates
        - If end_date is None, display as "Present"
        - Display URLs without https:// e.g. www.sahishnu.dev
    8. Output ONLY the LaTeX code, no explanation
    9. Ask the user for a version name, then save using modify_saved_resume() with action "add"
    10. If user saves, ask if they want to compile it to PDF using compile_resume() with the same version name
    """