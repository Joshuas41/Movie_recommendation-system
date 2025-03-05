from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Movie, Genre
from .schemas import MovieResponse, GenreResponse
from .recommendations import RecommendationEngine
from .database import get_db
from sqlalchemy.sql import extract


app = FastAPI(title="Movie Recommendation System")

@app.get("/movies", response_model=List[MovieResponse])
def get_movies(
    db: Session = Depends(get_db),
    genre: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0, le=10),
    year: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    query = db.query(Movie)

    if genre:
        query = query.join(Movie.genres).filter(Genre.name == genre)
    
    if min_rating:
        query = query.filter(Movie.vote_average >= min_rating)
    
    if year:
        query = query.filter(extract('year', Movie.release_date) == year)

    total = query.count()
    movies = (
        query.order_by(Movie.vote_average.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return movies

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