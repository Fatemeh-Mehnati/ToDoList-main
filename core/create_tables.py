# core/create_tables.py
from core.database import engine, Base
# Make sure to import all models so that the metadata includes them.
from core.models import task   # This import will load the models as well.
from core.models import project

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created")
