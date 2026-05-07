from db.models import create_db
from mcp_server.tools import mcp

def main():
    create_db()
    print("Connected to DB!")
    mcp.run(transport="sse", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
