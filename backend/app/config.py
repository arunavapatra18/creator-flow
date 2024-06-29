import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = (
    "postgresql://"
    + os.environ.get("POSTGRES_USER")
    + ":"
    + os.environ.get("POSTGRES_PASSWORD")
    + "@"
    + os.environ.get("POSTGRES_SERVER")
    + ":"
    + os.environ.get("POSTGRES_PORT")
    + "/"
    + os.environ.get("POSTGRES_DB")
)

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRY_MINUTES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRY_MINUTES"))

CORS_ORIGINS = [
    "http://localhost:5173",
    "https://localhost:5173",
    "http://127.0.0.1:5173",
    "https://127.0.0.1:5173",
]
