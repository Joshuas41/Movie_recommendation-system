import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hệ Thống Gợi Ý Phim", layout="wide")

st.title("🎬 Hệ Thống Gợi Ý Phim Thông Minh")

st.sidebar.header("🔍 Bộ Lọc Phim")

feature = st.sidebar.selectbox("Chọn Chức Năng", [
    "Khám Phá Phim", 
    "Gợi Ý Theo Phim", 
    "Gợi Ý Theo Thể Loại",
    "Thống Kê"
])

API_BASE_URL = "http://localhost:8000"

def fetch_movies(params=None):
    try:
        response = requests.get(f"{API_BASE_URL}/movies", params=params)
        return response.json()
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return []

def main_exploration():
    st.subheader("🌟 Khám Phá Phim")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        genre = st.selectbox("Thể Loại", ["Tất Cả", "Action", "Comedy", "Drama"])
    
    with col2:
        min_rating = st.slider("Điểm Tối Thiểu", 0.0, 10.0, 7.0)
    
    with col3:
        year = st.number_input("Năm", 2000, 2024, 2020)
    
    params = {
        "genre": genre if genre != "Tất Cả" else None,
        "min_rating": min_rating,
        "year": year
    }
    
    movies = fetch_movies(params)
    
    for movie in movies:
        col1, col2 = st.columns([1, 4])
        
        with col1:
            poster_url = f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}"
            st.image(poster_url if movie.get('poster_path') else "https://via.placeholder.com/200x300", width=150)
        
        with col2:
            st.write(f"**{movie['title']}** (Điểm: {movie['vote_average']})")
            st.write(movie['overview'])
        
        st.markdown("---")

def recommendation_by_movie():
    st.subheader("🎯 Gợi Ý Theo Phim")
    movie_id = st.number_input("Nhập ID Phim", min_value=1)
    
    if st.button("Xem Gợi Ý"):
        try:
            response = requests.get(f"{API_BASE_URL}/recommendations/movie/{movie_id}")
            recommendations = response.json()
            
            for movie in recommendations:
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    poster_url = f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}"
                    st.image(poster_url if movie.get('poster_path') else "https://via.placeholder.com/200x300", width=150)
                
                with col2:
                    st.write(f"**{movie['title']}** (Điểm: {movie['vote_average']})")
                    st.write(movie['overview'])
                
                st.markdown("---")
        except Exception as e:
            st.error(f"Lỗi: {e}")

def main():
    if feature == "Khám Phá Phim":
        main_exploration()
    elif feature == "Gợi Ý Theo Phim":
        recommendation_by_movie()

if __name__ == "__main__":
    main()