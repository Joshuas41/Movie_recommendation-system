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
    
    # Hiển thị một số phim có sẵn để người dùng chọn
    try:
        # Lấy 10 phim đầu tiên để gợi ý
        response = requests.get(f"{API_BASE_URL}/movies?page=1&page_size=10")
        available_movies = response.json()
        
        if available_movies:
            st.info("Gợi ý một số phim có sẵn trong hệ thống:")
            for movie in available_movies[:5]:  # Chỉ hiển thị 5 phim
                st.write(f"- ID: {movie['id']} - {movie['title']}")
    except Exception as e:
        st.warning(f"Không thể lấy danh sách phim gợi ý: {e}")
    
    movie_id = st.number_input("Nhập ID Phim", min_value=1)
    
    if st.button("Xem Gợi Ý"):
        with st.spinner("Đang tìm phim tương tự..."):
            try:
                # Thêm debug info
                st.info(f"Đang gọi API: {API_BASE_URL}/recommendations/movie/{movie_id}")
                
                response = requests.get(f"{API_BASE_URL}/recommendations/movie/{movie_id}")
                
                # Hiển thị thông tin response
                st.write("Status code:", response.status_code)
                
                if response.status_code != 200:
                    st.error(f"API trả về lỗi: {response.text}")
                    return
                
                recommendations = response.json()
                
                if not recommendations:
                    st.warning("Không tìm thấy phim tương tự. Có thể do phim này không có thể loại hoặc không có phim tương tự trong hệ thống.")
                    return
                
                st.success(f"Tìm thấy {len(recommendations)} phim tương tự!")
                
                for movie in recommendations:
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
                    
                    st.markdown("---")
            except Exception as e:
                st.error(f"Lỗi khi gọi API: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

def main():
    if feature == "Khám Phá Phim":
        main_exploration()
    elif feature == "Gợi Ý Theo Phim":
        recommendation_by_movie()

if __name__ == "__main__":
    main()