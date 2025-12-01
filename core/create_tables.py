# core/create_tables.py
from core.database import engine, Base
import core.models   # فقط همین برای لود همه مدل‌ها کافی است

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created")
