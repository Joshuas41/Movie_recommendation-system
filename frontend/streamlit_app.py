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
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            st.error(f"Định dạng dữ liệu không hợp lệ: {data}")
            return []
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return []

def main_exploration():
    st.subheader("🌟 Khám Phá Phim")
    # Debug: Kiểm tra dữ liệu API
    with st.expander("Debug API Data"):
        raw_data = fetch_movies()
        st.json(raw_data)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        genre = st.selectbox("Thể Loại", ["Tất Cả", "Action", "Comedy", "Drama", "Thriller", "Adventure"])
    
    with col2:
        min_rating = st.slider("Điểm Tối Thiểu", 0.0, 10.0, 7.0)
    
    with col3:
        year = st.number_input("Năm", 2000, 2024, 2020)
    
    params = {}
    if genre != "Tất Cả":
        params["genre"] = genre
    if min_rating > 0:
        params["min_rating"] = min_rating
    if year:
        params["year"] = year
    
    movies = fetch_movies(params)
    
    if not movies:
        st.warning("Không tìm thấy phim nào phù hợp với bộ lọc. Vui lòng thử lại với bộ lọc khác.")
    
    for movie in movies:
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if movie.get('poster_path'):
                poster_url = f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}"
                try:
                    st.image(poster_url, width=150)
                except:
                    st.image("https://via.placeholder.com/150x225?text=No+Poster", width=150)
            else:
                st.image("https://via.placeholder.com/150x225?text=No+Poster", width=150)
        
        with col2:
            st.write(f"**{movie['title']}** (Điểm: {movie.get('vote_average', 'N/A')})")
            st.write(movie.get('overview', 'Không có mô tả'))
            
            # Hiển thị thể loại
            if movie.get('genres'):
                genres_text = ", ".join([g['name'] for g in movie['genres']])
                st.write(f"**Thể loại:** {genres_text}")
        
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