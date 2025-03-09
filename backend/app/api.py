from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Movie, Genre
from .schemas import MovieResponse, GenreResponse
from .recommendations import RecommendationEngine
from .database import get_db
from sqlalchemy.sql import extract
from .models import Movie, Genre, MovieGenre

app = FastAPI(title="Movie Recommendation System")

from sqlalchemy import and_
from sqlalchemy.orm import joinedload

import traceback

from sqlalchemy.orm import joinedload

@app.get("/movies", response_model=List[MovieResponse])
def get_movies(
    db: Session = Depends(get_db),
    genre: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=10),
    year: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    query = db.query(Movie).options(joinedload(Movie.genres).joinedload(MovieGenre.genre))

    if genre:
        genre_obj = db.query(Genre).filter(Genre.name == genre).first()
        if genre_obj:
            query = query.join(Movie.genres).filter(MovieGenre.genre_id == genre_obj.id)

    if min_rating is not None:
        query = query.filter(Movie.vote_average >= min_rating)

    if year:
        query = query.filter(extract('year', Movie.release_date) == year)

    movies = (
        query.order_by(Movie.vote_average.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    # Chuyển đổi dữ liệu thành định dạng phù hợp với MovieResponse
    result = []
    for movie in movies:
        genre_list = [{"id": mg.genre.id, "name": mg.genre.name} for mg in movie.genres]
        movie_dict = {
            "id": movie.id,
            "title": movie.title,
            "overview": movie.overview,
            "vote_average": movie.vote_average,
            "release_date": movie.release_date,
            "poster_path": movie.poster_path,
            "genres": genre_list
        }
        result.append(movie_dict)

    return result
@app.get("/recommendations/movie/{movie_id}", response_model=List[MovieResponse])
def get_movie_recommendations(
    movie_id: int, 
    db: Session = Depends(get_db),
    top_n: int = Query(10, ge=1, le=50)
):
    recommendation_engine = RecommendationEngine(db)
    recommendations = recommendation_engine.get_content_based_recommendations(movie_id, top_n)
    return recommendations

@app.get("/recommendations/genre/{genre_name}", response_model=List[MovieResponse])
def get_genre_recommendations(
    genre_name: str, 
    db: Session = Depends(get_db),
    top_n: int = Query(10, ge=1, le=50)
):
    recommendation_engine = RecommendationEngine(db)
    recommendations = recommendation_engine.get_genre_recommendations(genre_name, top_n)
    return recommendations



@app.get("/debug/movie-genres")
def debug_movie_genres(db: Session = Depends(get_db)):
    # Lấy một số bản ghi để kiểm tra mối quan hệ
    movie_genres = db.query(MovieGenre).join(Movie).join(Genre).limit(10).all()
    return [
        {
            "movie_id": mg.movie_id, 
            "movie_title": mg.movie.title,
            "genre_id": mg.genre_id,
            "genre_name": mg.genre.name
        } for mg in movie_genres
    ]
    
@app.get("/debug/filter-check")
def debug_filter_check(
    db: Session = Depends(get_db),
    genre: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None),
    year: Optional[int] = Query(None)
):
    # Kiểm tra từng điều kiện
    genre_obj = db.query(Genre).filter(Genre.name == genre).first() if genre else None
    
    return {
        "genre_input": genre,
        "genre_found": {"id": genre_obj.id, "name": genre_obj.name} if genre_obj else None,
        "min_rating": min_rating,
        "year": year
    }
@app.get("/debug/movie/{movie_id}")
def debug_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return {"error": f"Movie with ID {movie_id} not found"}
    
    movie_genres = db.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).all()
    genre_ids = [mg.genre_id for mg in movie_genres]
    genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all() if genre_ids else []
    
    return {
        "movie": {
            "id": movie.id,
            "title": movie.title,
            "vote_average": movie.vote_average
        },
        "genres": [{"id": g.id, "name": g.name} for g in genres],
        "genre_count": len(genres)
    }