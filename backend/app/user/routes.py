from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from db.database import get_session
from user.auth import get_current_user
from user.controller import (
    login_user,
    register_user,
)
from user.models import (
    UserCreate,
    UserResponseModel,
    Token,
)

user_router = APIRouter()


@user_router.post("/register", response_model=UserResponseModel)
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user_response = register_user(user, session)

    return db_user_response


@user_router.post("/login", response_model=Token)
def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    token = login_user(login_data, session)

    return token


@user_router.get("/me", response_model=UserResponseModel)
def get_user(user=Depends(get_current_user)):
    return user
