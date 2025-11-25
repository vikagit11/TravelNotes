import os 

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./travelnotes.db")   # путь к базе данных
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")