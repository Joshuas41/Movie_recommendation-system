from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db
from .api import app as api_router

# Tạo ứng dụng FastAPI chính
app = FastAPI(title="Movie Recommendation System")

# Gắn router từ api.py
app.mount("/", api_router)

# Thêm các route bổ sung nếu cần
@app.post("/movies/", response_model=schemas.MovieResponse)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db=db, movie=movie)

@app.post("/genres/", response_model=schemas.GenreResponse)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    return crud.create_genre(db=db, genre=genre)

# Route để kết nối movie với genre
@app.post("/movie-genres/")
def create_movie_genre(movie_id: int, genre_id: int, db: Session = Depends(get_db)):
    return crud.create_movie_genre(db=db, movie_id=movie_id, genre_id=genre_id)