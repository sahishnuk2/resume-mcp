# for add, update, delete logic of projects, work exp, education...
from datetime import datetime
from db.models import Project, Work, engine
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