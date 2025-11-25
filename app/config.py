import os 

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./travelnotes.db")   #путь к базе данных
DEBUG = True
