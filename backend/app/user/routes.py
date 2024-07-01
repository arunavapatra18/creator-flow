from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from db.database import get_session
from user.auth import get_current_user
from user.controller import (
    login_user,
    register_user,
    set_youtube_api,
    update_user_data,
)
from user.models import (
    CreatorAPIUpdateModel,
    Token,
    UserCreate,
    UserResponseModel,
    UserUpdateModel,
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
    response = login_user(login_data, session)

    return response


@user_router.get("/me", response_model=UserResponseModel)
def get_user(user=Depends(get_current_user)):
    return user


@user_router.patch("/update_apikey")
def update_creator_youtube_api(
    api_model: CreatorAPIUpdateModel,
    user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return set_youtube_api(api_model, user, session)


@user_router.patch("/update_user")
def update_user(
    user_update_model: UserUpdateModel,
    user=Depends(get_current_user),
    session=Depends(get_session),
):
    return update_user_data(user_update_model, user, session)
