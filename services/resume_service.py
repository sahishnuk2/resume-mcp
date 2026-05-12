# for add, update, delete logic of projects, work exp, education...
from datetime import datetime
from db.models import PersonalInfo, Project, Work, Skill, SavedResume, Education, EducationAchievement, RelevantCourse, engine
from sqlmodel import Session, select

# Projects
def add_project(name: str,
                description: str, 
                tech_stack: str,
                start_date: str, 
                end_date: str| None = None,
                link: str | None = None
                ):
    try:
        start = datetime.strptime(start_date, "%b %Y").date()
        end = datetime.strptime(end_date, "%b %Y").date() if end_date else None
        project = Project(name=name, description=description, tech_stack=tech_stack, 
                        start_date=start, end_date=end, link=link)
        with Session(engine) as session:
            session.add(project)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to add project: " + str(e))
    
def delete_project(name: str):
    try:
        with Session(engine) as session:
            statement = select(Project).where(Project.name == name)
            project = session.exec(statement).first()
            if not project:
                raise ValueError("Project not found in database")
            session.delete(project)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to delete project: " + str(e))
    
def update_project(name: str,
                description: str | None = None, 
                tech_stack: str | None = None,
                start_date: str | None = None, 
                end_date: str| None = None,
                link: str | None = None
                ):
    try:
        with Session(engine) as session:
            statement = select(Project).where(Project.name == name)
            project = session.exec(statement).first()

            if not project:
                raise ValueError("Project not found in database")
            
            if description:
                project.description = description
            if tech_stack:
                project.tech_stack = tech_stack
            if link:
                project.link = link
            if start_date:
                project.start_date = datetime.strptime(start_date, "%b %Y").date()
            if end_date:
                project.end_date = datetime.strptime(end_date, "%b %Y").date()

            session.add(project)
            session.commit()
            session.refresh(project)

    except Exception as e:
        raise ValueError("Failed to update project: " + str(e))
    
# Work Experience
def add_work(company: str,
            role: str,
            description: str, 
            start_date: str, 
            end_date: str| None = None,
            ):
    try:
        start = datetime.strptime(start_date, "%b %Y").date()
        end = datetime.strptime(end_date, "%b %Y").date() if end_date else None
        work = Work(company=company, role=role, description=description,
                        start_date=start, end_date=end)
        with Session(engine) as session:
            session.add(work)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to add work experience: " + str(e))

def delete_work(company: str):
    try:
        with Session(engine) as session:
            statement = select(Work).where(Work.company == company)
            work = session.exec(statement).first()
            if not work:
                raise ValueError("Work Experience not found in database")
            session.delete(work)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to delete work experience: " + str(e))
    
def update_work(company: str,
                role: str | None = None,
                description: str | None = None, 
                start_date: str | None = None, 
                end_date: str| None = None,
                ):
    try:
        with Session(engine) as session:
            statement = select(Work).where(Work.company == company)
            work = session.exec(statement).first()

            if not work:
                raise ValueError("Work Experience not found in database")
            
            if description:
                work.description = description
            if role:
                work.role = role
            if start_date:
                work.start_date = datetime.strptime(start_date, "%b %Y").date()
            if end_date:
                work.end_date = datetime.strptime(end_date, "%b %Y").date()

            session.add(work)
            session.commit()
            session.refresh(work)

    except Exception as e:
        raise ValueError("Failed to update work experience: " + str(e))

# Skills
def add_skill(name: str, category: str):
    try:
        skill = Skill(name=name, category=category)
        with Session(engine) as session:
            session.add(skill)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to add skill: " + str(e))

def delete_skill(name: str):
    try:
        with Session(engine) as session:
            statement = select(Skill).where(Skill.name == name)
            skill = session.exec(statement).first()
            if not skill:
                raise ValueError("Skill not found in database")
            session.delete(skill)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to delete skill: " + str(e))

def update_skill(name: str, category: str | None = None):
    try:
        with Session(engine) as session:
            statement = select(Skill).where(Skill.name == name)
            skill = session.exec(statement).first()
            if not skill:
                raise ValueError("Skill not found in database")
            if category:
                skill.category = category
            session.add(skill)
            session.commit()
            session.refresh(skill)
    except Exception as e:
        raise ValueError("Failed to update skill: " + str(e))

# Education
def update_education(institution: str | None = None,
                     degree: str | None = None,
                     field: str | None = None,
                     minor: str | None = None,
                     start_date: str | None = None,
                     end_date: str | None = None,
                     gpa: str | None = None
                     ):
    try:
        with Session(engine) as session:
            education = session.exec(select(Education)).first()
            if not education:
                raise ValueError("Education not found in database")
            if institution:
                education.institution = institution
            if degree:
                education.degree = degree
            if field:
                education.field = field
            if minor:
                education.minor = minor
            if gpa:
                education.gpa = float(gpa)
            if start_date:
                education.end_date = datetime.strptime(start_date, "%b %Y").date()
            if end_date:
                education.end_date = datetime.strptime(end_date, "%b %Y").date()
            session.add(education)
            session.commit()
            session.refresh(education)
    except Exception as e:
        raise ValueError("Failed to update education: " + str(e))

# Education Achievement
def add_education_achievement(achievement: str):
    try:
        with Session(engine) as session:
            education = session.exec(select(Education)).first()
            if not education:
                raise ValueError("Education not found in database")
            edu_achievement = EducationAchievement(education_id=education.id, achievement=achievement)
            session.add(edu_achievement)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to add education achievement: " + str(e))

def delete_education_achievement(achievement: str):
    try:
        with Session(engine) as session:
            statement = select(EducationAchievement).where(EducationAchievement.achievement == achievement)
            edu_achievement = session.exec(statement).first()
            if not edu_achievement:
                raise ValueError("Education achievement not found in database")
            session.delete(edu_achievement)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to delete education achievement: " + str(e))

def update_education_achievement(achievement: str, new_achievement: str):
    try:
        with Session(engine) as session:
            statement = select(EducationAchievement).where(EducationAchievement.achievement == achievement)
            edu_achievement = session.exec(statement).first()
            if not edu_achievement:
                raise ValueError("Education achievement not found in database")
            edu_achievement.achievement = new_achievement
            session.add(edu_achievement)
            session.commit()
            session.refresh(edu_achievement)
    except Exception as e:
        raise ValueError("Failed to update education achievement: " + str(e))

# Relevant Courses
def add_relevant_course(course_name: str, grade: str | None):
    try:
        with Session(engine) as session:
            education = session.exec(select(Education)).first()
            if not education:
                raise ValueError("Education not found in database")
            course = RelevantCourse(education_id=education.id, course_name=course_name, grade=grade)
            session.add(course)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to add relevant course: " + str(e))

def delete_relevant_course(course_name: str):
    try:
        with Session(engine) as session:
            statement = select(RelevantCourse).where(RelevantCourse.course_name == course_name)
            course = session.exec(statement).first()
            if not course:
                raise ValueError("Relevant course not found in database")
            session.delete(course)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to delete relevant course: " + str(e))

def update_relevant_course(course_name: str, grade: str | None = None):
    try:
        with Session(engine) as session:
            statement = select(RelevantCourse).where(RelevantCourse.course_name == course_name)
            course = session.exec(statement).first()
            if not course:
                raise ValueError("Relevant course not found in database")
            if grade:
                course.grade = grade
            session.add(course)
            session.commit()
            session.refresh(course)
    except Exception as e:
        raise ValueError("Failed to update relevant course: " + str(e))

# Saved Resume
def add_saved_resume(version_name: str, content: str):
    try:
        resume = SavedResume(version_name=version_name, content=content)
        with Session(engine) as session:
            session.add(resume)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to add saved resume: " + str(e))

def delete_saved_resume(version_name: str):
    try:
        with Session(engine) as session:
            statement = select(SavedResume).where(SavedResume.version_name == version_name)
            resume = session.exec(statement).first()
            if not resume:
                raise ValueError("Saved resume not found in database")
            session.delete(resume)
            session.commit()
    except Exception as e:
        raise ValueError("Failed to delete saved resume: " + str(e))

def update_saved_resume(version_name: str, content: str | None = None):
    try:
        with Session(engine) as session:
            statement = select(SavedResume).where(SavedResume.version_name == version_name)
            resume = session.exec(statement).first()
            if not resume:
                raise ValueError("Saved resume not found in database")
            if content:
                resume.content = content
            session.add(resume)
            session.commit()
            session.refresh(resume)
    except Exception as e:
        raise ValueError("Failed to update saved resume: " + str(e))

# Get all data
def get_all_data():
    try:
        with Session(engine) as session:
            projects = session.exec(select(Project)).all()
            works = session.exec(select(Work)).all()
            skills = session.exec(select(Skill)).all()
            education = session.exec(select(Education)).all()
            eduachievements = session.exec(select(EducationAchievement)).all()
            rcourses = session.exec(select(RelevantCourse)).all()
            personal_info = session.exec(select(PersonalInfo)).first()

            return {
                "personal_info": personal_info.model_dump() if personal_info else None,
                "projects": [p.model_dump() for p in projects],
                "work": [w.model_dump() for w in works],
                "skills": [s.model_dump() for s in skills],
                "education": [e.model_dump() for e in education],
                "education_achievements": [ea.model_dump() for ea in eduachievements],
                "relevant_courses": [rc.model_dump() for rc in rcourses]
            }

    except Exception as e:
        raise ValueError("Database Error: " + str(e))

# Peronal Info
def update_personal(name: str | None = None,
                     phone: str | None = None,
                     email: str | None = None,
                     website: str | None = None,
                     github: str | None = None,
                     linkedin: str | None = None
                     ):
    try:
        with Session(engine) as session:
            info = session.exec(select(PersonalInfo)).first()
            if not info:
                raise ValueError("Personal Information not found in database")
            if name:
                info.name = name
            if phone:
                info.phone = phone
            if email:
                info.email = email
            if website:
                info.website = website
            if github:
                info.github = github
            if linkedin:
                info.linkedin = linkedin
            session.add(info)
            session.commit()
            session.refresh(info)
    except Exception as e:
        raise ValueError("Failed to update personal information: " + str(e))

# Resumes
def get_resumes():
    with Session(engine) as session:
        statement = select(SavedResume.version_name)
        resumes = session.exec(statement).all()
        return resumes

def get_resume(version_name: str):
    with Session(engine) as session:
        statement = select(SavedResume).where(SavedResume.version_name == version_name)
        resume = session.exec(statement).first()
        return resume.content