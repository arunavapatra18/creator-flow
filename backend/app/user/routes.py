from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from db.database import get_session
from user.auth import get_current_user
from user.controller import (
    delete_current_user,
    get_all_creators,
    get_all_editors,
    login_user,
    register_user,
    set_youtube_apikey,
    update_user_data,
)
from user.models import (
    CreatorAPIUpdateModel,
    GetCreatorsResponseModel,
    GetEditorsResponseModel,
    Token,
    User,
    UserCreate,
    UserResponseModel,
    UserUpdateModel,
)

user_router = APIRouter(prefix="/user")


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
def get_user(user: User = Depends(get_current_user)):
    return user


@user_router.patch("/update_apikey")
def update_creator_youtube_apikey(
    api_model: CreatorAPIUpdateModel,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return set_youtube_apikey(api_model, user, session)


@user_router.patch("/update")
def update_user(
    user_update_model: UserUpdateModel,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return update_user_data(user_update_model, user, session)


@user_router.delete("/delete")
def delete_user(
    user: User = Depends(get_current_user), session: Session = Depends(get_session)
):
    return delete_current_user(user, session)


@user_router.get("/editors", response_model=GetEditorsResponseModel)
def get_editors(session: Session = Depends(get_session)):
    return get_all_editors(session)


@user_router.get("/creators", response_model=GetCreatorsResponseModel)
def get_creators(session: Session = Depends(get_session)):
    return get_all_creators(session)
