from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")  # Kiểm tra giá trị có bị None không

DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL:", DATABASE_URL)

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Kết nối database thành công!")
    connection.close()
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
