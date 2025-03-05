import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from typing import List, Dict
from .models import Movie, Genre, MovieGenre

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_content_based_recommendations(self, movie_id: int, top_n: int = 10) -> List[Dict]:
        # Lấy thể loại của phim gốc
        movie_genres = self.db.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).all()
        genre_ids = [mg.genre_id for mg in movie_genres]

        # Tìm các phim có thể loại tương đồng
        similar_movies = (
            self.db.query(Movie, MovieGenre)
            .join(MovieGenre, Movie.id == MovieGenre.movie_id)
            .filter(MovieGenre.genre_id.in_(genre_ids))
            .filter(Movie.id != movie_id)
            .order_by(Movie.vote_average.desc())
            .limit(top_n)
            .all()
        )

        # Chuyển đổi kết quả
        recommendations = [
            {
                "id": movie.id,
                "title": movie.title,
                "vote_average": movie.vote_average,
                "overview": movie.overview,
                "poster_path": movie.poster_path
            } for movie, _ in similar_movies
        ]

        return recommendations

    def get_genre_recommendations(self, genre_name: str, top_n: int = 10) -> List[Dict]:
        # Lấy ID thể loại
        genre = self.db.query(Genre).filter(Genre.name == genre_name).first()
        
        if not genre:
            return []

        # Tìm các phim thuộc thể loại
        recommended_movies = (
            self.db.query(Movie, MovieGenre)
            .join(MovieGenre, Movie.id == MovieGenre.movie_id)
            .filter(MovieGenre.genre_id == genre.id)
            .order_by(Movie.vote_average.desc())
            .limit(top_n)
            .all()
        )

        # Chuyển đổi kết quả
        recommendations = [
            {
                "id": movie.id,
                "title": movie.title,
                "vote_average": movie.vote_average,
                "overview": movie.overview,
                "poster_path": movie.poster_path
            } for movie, _ in recommended_movies
        ]

        return recommendations