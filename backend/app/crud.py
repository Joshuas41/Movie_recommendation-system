from sqlalchemy.orm import Session
from . import models, schemas

def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_movies(
    db: Session, 
    genre: str = None, 
    min_rating: float = None, 
    year: int = None,
    skip: int = 0, 
    limit: int = 100
):
    query = db.query(models.Movie)
    
    if genre:
        query = query.join(models.MovieGenre).join(models.Genre).filter(models.Genre.name == genre)
    
    if min_rating:
        query = query.filter(models.Movie.vote_average >= min_rating)
    
    if year:
        query = query.filter(models.Movie.release_date.year == year)
    
    return query.offset(skip).limit(limit).all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def create_movie_genre(db: Session, movie_id: int, genre_id: int):
    db_movie_genre = models.MovieGenre(movie_id=movie_id, genre_id=genre_id)
    db.add(db_movie_genre)
    db.commit()
    return db_movie_genre