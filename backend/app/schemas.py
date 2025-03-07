from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class GenreBase(BaseModel):
    name: str
    id: int


class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    id: int
    title: str
    overview: str
    vote_average: float
    release_date: date
    poster_path: Optional[str] = None
    genres: List[GenreBase] = []

class MovieCreate(MovieBase):
    pass

from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class GenreBase(BaseModel):
    id: int
    name: str

class MovieResponse(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    vote_average: Optional[float] = None
    release_date: Optional[date] = None
    poster_path: Optional[str] = None
    genres: List[GenreBase] = []

    class Config:
        orm_mode = True