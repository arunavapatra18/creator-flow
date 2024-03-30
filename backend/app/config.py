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
