from fastapi import FastAPI
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

def create_application() -> FastAPI:
    app = FastAPI(title="Movie Recommendation System")
    return app