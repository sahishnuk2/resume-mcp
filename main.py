from db.models import create_db

def main():
    create_db()
    print("Connected to DB!")


if __name__ == "__main__":
    main()
