from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

import user.auth as auth
from user.models import Creator, User, UserCreate, UserResponseModel
from user.util import generate_password_hash, verify_password


def register_user(user: UserCreate, session: Session):
    """Register a new User to database

    Args:
        user (UserCreate): User to add
        session (Session): DB Session

    Raises:
        HTTPException: 409 Email already taken

    Returns:
        UserResponseModel: _description_
    """

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

    if db_user.role == "CREATOR":
        db_user_role = Creator(user_id=db_user.id)
        session.add(db_user_role)
        session.commit()

    return UserResponseModel(
        email=db_user.email, id=db_user.id, name=db_user.name, role=db_user.role
    )


def login_user(user_detail: OAuth2PasswordRequestForm, session: Session):
    """Authenticate and login a User

    Args:
        user_detail (OAuth2PasswordRequestForm): Form data for username and password
        .
        session (Session): DB Session

    Raises:
        HTTPException: 401 Email doesnot exist
        HTTPException: 401 Passwords do not match

    Returns:
        Response: JWT
    """

    user: User = session.exec(
        select(User).filter(User.email == user_detail.username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"The {user_detail.username} does not exist",
        )

    user.id = str(user.id)

    if not verify_password(user_detail.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"The passwords do not match",
        )

    access_token = auth.create_access_token(data={"user_id": user.id})

    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie(
        "access_token", access_token, httponly=True, secure=True, samesite="none"
    )

    return response
