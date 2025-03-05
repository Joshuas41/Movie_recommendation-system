from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    vote_average = Column(Float)
    release_date = Column(Date)
    poster_path = Column(String, nullable=True)  # Thêm trường này
    genres = relationship("MovieGenre", back_populates="movie")
    
class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship("MovieGenre", back_populates="genre")

class MovieGenre(Base):
    __tablename__ = "movie_genres"
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)
    movie = relationship("Movie", back_populates="genres")
    genre = relationship("Genre", back_populates="movies")