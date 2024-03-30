from fastapi import FastAPI

from db.database import close_db, create_db_and_tables
from user.routes import user_router

app = FastAPI(title="creator-flow")

app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
def on_shutdown():
    close_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
