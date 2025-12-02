# core/create_tables.py
from core.database import engine, Base
import core.models   # That's enough to load all models.

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created")
