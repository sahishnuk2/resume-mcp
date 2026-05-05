from db.models import create_db
from mcp.tools import mcp

def main():
    create_db()
    print("Connected to DB!")
    mcp.run()


if __name__ == "__main__":
    main()
