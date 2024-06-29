from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

import user.auth as auth
from user.models import Creator, Token, User, UserCreate, UserResponseModel
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

    user = session.exec(select(User).filter(User.email == user_detail.username)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The {user_detail.username} does not exist",
        )

    user_id = str(user.id)

    if not verify_password(user_detail.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The passwords do not match",
        )

    user.disabled = False

    session.add(user)
    session.commit()

    access_token = auth.create_access_token(data={"user_id": user_id})

    response = Token(access_token=access_token)

    return response
