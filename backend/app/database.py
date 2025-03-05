from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
from backend.app.database import SessionLocal
from backend.app.models import Movie

def check_movies():
    db = SessionLocal()
    try:
        movies = db.query(Movie).all()
        print(f"Số lượng phim: {len(movies)}")
    except Exception as e:
        print(f"Lỗi truy vấn: {e}")
    finally:
        db.close()

check_movies()