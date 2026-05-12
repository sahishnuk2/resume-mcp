# Resume MCP

An MCP server that connects to Claude Desktop to generate tailored LaTeX resumes from your personal data stored in a PostgreSQL database.

---

## Setup (Local / Main Branch)

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- Docker Desktop (for the database)
- pdflatex (for PDF compilation)

### 1. Install pdflatex

**macOS:**
```bash
brew install --cask mactex-no-gui
```

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-latex-recommended texlive-latex-extra
```

**Windows:**
Download and install [MiKTeX](https://miktex.org/download). During installation, set it to install missing packages automatically.

### 2. Clone and install dependencies

```bash
git clone <repo-url>
cd resume-mcp
uv sync
```

### 3. Configure environment

Create a `.env` file:

```
DB_PASSWORD='yourpassword'
POSTGRESQL_URL='postgresql://yourusername:yourpassword@localhost:5431/resume_db'
OUTPUT_DIR=/path/to/save/pdfs
```

### 4. Start the database

```bash
docker compose up -d db
```

### 5. Seed your data

Create `db/seed.py` with your details:

```python
from services.resume_service import (
    add_project, add_work, add_skill,
    add_education_achievement, add_relevant_course, update_personal
)

def seed():
    # ── Skills ─────────────────────────────────────────────────────
    for lang in ["Python", "Java", "Go"]:
        add_skill(name=lang, category="Languages")

    for tool in ["Git", "Docker"]:
        add_skill(name=tool, category="Tools & Platforms")

    # ── Education Achievements ─────────────────────────────────────
    add_education_achievement("Dean's List AY24/25")

    # ── Relevant Courses ───────────────────────────────────────────
    add_relevant_course("Data Structures & Algorithms", "A")
    add_relevant_course("Computer Networks", None)  # None if in progress

    # ── Projects ───────────────────────────────────────────────────
    add_project(
        name="My Project",
        description="What it does and what you achieved.",
        tech_stack="Python, PostgreSQL",
        start_date="Jan 2025",
        end_date="May 2025",
        link="https://github.com/yourusername/project"
    )

    # ── Work Experience ────────────────────────────────────────────
    add_work(
        company="Company Name",
        role="Your Role",
        description="What you did and achieved.",
        start_date="Jun 2024",
        end_date="Dec 2024"  # Use None for present
    )

if __name__ == "__main__":
    seed()
```

Then run:

```bash
uv run python -m db.seed
```

**Education and personal info must be inserted manually** as they are single-record tables. Connect to the database:

```bash
docker exec -it resume-mcp-db-1 psql -U yourusername -d resume_db
```

Then insert your data:

```sql
INSERT INTO personalinfo (name, phone, email, website, linkedin, github)
VALUES (
    'Your Name',
    '+00 00000000',
    'you@email.com',
    'https://www.yoursite.com',
    'https://www.linkedin.com/in/yourprofile',
    'https://github.com/yourusername'
);

INSERT INTO education (institution, degree, field, minor, start_date, end_date, gpa)
VALUES (
    'Your University',
    'Bachelor of ...',
    'Computer Science',
    'Your Minor',
    '2022-08-01',
    '2026-05-01',
    4.5
);
```

### 6. Connect to Claude Desktop

Open Claude Desktop → Settings → Developer → Edit Config. This opens `claude_desktop_config.json`. Add the following inside `mcpServers`, then restart Claude Desktop:

```json
{
  "mcpServers": {
    "resume-mcp": {
      "command": "/path/to/resume-mcp/.venv/bin/python",
      "args": ["/path/to/resume-mcp/main.py"],
      "cwd": "/path/to/resume-mcp"
    }
  }
}
```

---

## Customising the Resume Prompt

The resume generation prompt is in `mcp_server/tools.py` inside the `generate_resume` function docstring (~line 299). Edit the rules there to change section order, formatting, or any instructions passed to Claude when generating your resume.

---

## Docker Deployment

Use the `docker-deploy` branch for a fully containerised setup (app + database).

### Prerequisites
- Docker Desktop
- Node.js / npm (for mcp-remote)

### 1. Switch branch and build

```bash
git checkout docker-deploy
docker compose up -d --build
```

### 2. Connect to Claude Desktop

Install the SSE bridge:

```bash
npm install -g mcp-remote
```

Open Claude Desktop → Settings → Developer → Edit Config. Add the following inside `mcpServers`, then restart Claude Desktop:

```json
{
  "mcpServers": {
    "resume-mcp": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8000/sse"]
    }
  }
}
```

### 3. Seed your data

```bash
docker exec -it resume-mcp-app-1 uv run python -m db.seed
```

For education and personal info, exec into the database container and run the same `INSERT` statements as above:

```bash
docker exec -it resume-mcp-db-1 psql -U yourusername -d resume_db
```

### Next time you want to use it

```bash
docker compose up -d
```
