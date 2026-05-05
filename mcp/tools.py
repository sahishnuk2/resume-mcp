from fastmcp import FastMCP
from pydantic import BaseModel
from services.resume_service import add_project, delete_project, update_project

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
            return "Action must be 'add', 'delete' or 'update' only'"
        return "Projects tables updated"
    except Exception as e:
        return "Error: " + str(e)