import os
import sys
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dotenv

# Thêm đường dẫn để import từ backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.models import Base, Movie, Genre, MovieGenre
from backend.app.database import engine

# Load biến môi trường
dotenv.load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Tạo session
SessionLocal = sessionmaker(bind=engine)

def fetch_movies_from_tmdb(page=1):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page}"
    response = requests.get(url)
    return response.json().get('results', [])

def fetch_movie_genres():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return response.json().get('genres', [])

def save_data():
    # Tạo các bảng
    Base.metadata.create_all(bind=engine)
    
    # Tạo session
    db = SessionLocal()

    try:
        # Lưu thể loại
        genres_data = fetch_movie_genres()
        for genre_info in genres_data:
            existing_genre = db.query(Genre).filter(Genre.id == genre_info['id']).first()
            if not existing_genre:
                genre = Genre(id=genre_info['id'], name=genre_info['name'])
                db.add(genre)
        
        db.commit()

        # Lấy và lưu phim
        for page in range(1, 6):  # Lấy 5 trang
            movies_data = fetch_movies_from_tmdb(page)
            
            for movie_info in movies_data:
                # Kiểm tra phim đã tồn tại chưa
                existing_movie = db.query(Movie).filter(Movie.id == movie_info['id']).first()
                if existing_movie:
                    continue

                # Tạo phim mới
                movie = Movie(
                    id=movie_info['id'],
                    title=movie_info['title'],
                    overview=movie_info['overview'],
                    vote_average=movie_info['vote_average'],
                    release_date=movie_info.get('release_date'),
                    poster_path=movie_info.get('poster_path')
                )
                db.add(movie)

                # Lưu mối quan hệ thể loại
                for genre_id in movie_info.get('genre_ids', []):
                    movie_genre = MovieGenre(movie_id=movie.id, genre_id=genre_id)
                    db.add(movie_genre)

        db.commit()
        print("✅ Dữ liệu đã được lưu thành công!")

    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    save_data()