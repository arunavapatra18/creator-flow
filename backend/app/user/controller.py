from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

import user.auth as auth
from user.models import Creator, Editor, Token, User, UserCreate, UserResponseModel
from user.util import generate_password_hash, verify_password


def register_user(user: UserCreate, session: Session):
    # Check if email already exisits
    email_taken = session.exec(select(User).where(User.email == user.email))
    if email_taken.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    # Hash password before storing to database
    user.password = generate_password_hash(user.password)

    # Validate User model
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    if db_user.role == "creator":
        # Create a corresponding Creator/Editor model
        db_user_role = Creator(user_id=db_user.id)
    else:
        db_user_role = Editor(user_id=db_user.id)

    session.add(db_user_role)
    session.commit()

    return UserResponseModel(
        email=db_user.email, id=db_user.id, name=db_user.name, role=db_user.role
    )


def login_user(user_detail: OAuth2PasswordRequestForm, session: Session):
    user: User = session.exec(
        select(User).filter(User.email == user_detail.username)
    ).first()
    user.id = str(user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"The {user_detail.username} does not exist",
        )

    if not verify_password(user_detail.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"The passwords do not match",
        )

    access_token = auth.create_access_token(data={"user_id": user.id})

    return Token(access_token=access_token, token_type="bearer")
