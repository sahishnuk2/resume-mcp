# for add, update, delete logic of projects, work exp, education...
from datetime import datetime
from db.models import Project, engine
from sqlmodel import Session, select

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