from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from user.controller import register_creator, register_editor
from user.models import CreatorCreate, EditorCreate, UserCreate, UserResponseModel

user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model=UserResponseModel)
def register(user: UserCreate, session: Session = Depends(get_session)):
    if user.role == "Creator":
        db_user = register_creator(
            CreatorCreate(email=user.email, name=user.name, password=user.password),
            session,
        )
    else:
        db_user = register_editor(
            EditorCreate(email=user.email, name=user.name, password=user.password),
            session,
        )
    return UserResponseModel(email=db_user.email, id=db_user.id, name=db_user.name)
