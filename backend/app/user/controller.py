from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

import user.auth as auth
from user.models import (
    Creator,
    CreatorAPIUpdateModel,
    GetCreatorsResponseModel,
    GetEditorsResponseModel,
    Token,
    User,
    UserCreate,
    UserResponseModel,
    UserUpdateModel,
)
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

    access_token = auth.create_access_token(data={"user_id": user_id})

    response = Token(access_token=access_token)

    return response


def set_youtube_apikey(api_model: CreatorAPIUpdateModel, user: User, session: Session):
    """Set youtube api key for creator

    Args:
        api_model (CreatorAPIUpdateModel): Model for youtube api key
        user (User): Current user
        session (Session): Database session

    Raises:
        HTTPException: 404 Creator doesnot exist

    Returns:
        JSONResponse: Success/failure to save api key to database
    """
    if user and user.role == "CREATOR":
        creator = session.exec(
            select(Creator).filter(Creator.user_id == user.id)
        ).first()

        if not creator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The creator {user.name} doesnot exists.",
            )

        creator.youtube_api_key = generate_password_hash(api_model.youtube_api_key)
        try:
            session.commit()
            session.refresh(creator)
            return JSONResponse(
                status_code=status.HTTP_200_OK, content="Youtube API set successfully!"
            )
        except:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Failed to save to database!",
            )


def update_user_data(user_update_model: UserUpdateModel, user: User, session: Session):
    """Update user data in database

    Args:
        user_update_model (UserUpdateModel): Model for user details update
        user (User): Current user
        session (Session): Database session

    Raises:
        HTTPException: 404 User not found

    Returns:
        JSONResponse: Success/failure to save user updates to database
    """
    db_user = session.exec(select(User).filter(User.id == user.id)).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found!"
        )

    if user_update_model.name is not None and user_update_model.name != db_user.name:
        db_user.name = user_update_model.name
    if user_update_model.email is not None and user_update_model.email != db_user.email:
        db_user.email = user_update_model.email
    if (
        user_update_model.password is not None
        and verify_password(user_update_model.password, db_user.password) is False
    ):
        db_user.password = generate_password_hash(user_update_model.password)

    try:
        session.commit()
        session.refresh(db_user)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content="User data updated successfully!"
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Failed to save to database!",
        )


def delete_current_user(user: User, session: Session):
    """Delete current user

    Args:
        user (User): current user
        session (Session): database session

    Raises:
        HTTPException: 404 User not found

    Returns:
        JSONResponse: Success/failure to delete the current user
    """
    db_user = session.exec(select(User).filter(User.id == user.id)).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found!"
        )

    try:
        session.delete(db_user)
        session.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK, content="User deleted successfully!"
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Failed to save to database!",
        )


def get_all_editors(session: Session):
    """Get all the editors

    Args:
        session (Session): database session

    Raises:
        HTTPException: 404 No editors are found

    Returns:
        GetEditorsResponseModel: List of editors
    """
    editors = session.exec(select(User).filter(User.role == "EDITOR"))

    if not editors:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Editors not found!"
        )

    return GetEditorsResponseModel(editors=editors)


def get_all_creators(session: Session):
    """Get all the creators

    Args:
        session (Session): database session

    Raises:
        HTTPException: 404 No creators are found

    Returns:
        GetCreatorsResponseModel: List of creators
    """
    creators = session.exec(select(User).filter(User.role == "CREATOR"))

    if not creators:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Creators not found!"
        )

    return GetCreatorsResponseModel(creators=creators)
