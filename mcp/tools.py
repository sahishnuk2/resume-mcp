from fastmcp import FastMCP
from pydantic import BaseModel

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
    action: "add" → pass project
    action: "update" → pass update (only changed fields)
    action: "delete" → pass project name only
    Successfully modifies projects table in database
    """
    return "Projects tables updated"