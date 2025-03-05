from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    overview: Optional[str] = None
    vote_average: Optional[float] = None
    release_date: Optional[date] = None
    poster_path: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    genres: List[GenreResponse] = []

    class Config:
        orm_mode = True