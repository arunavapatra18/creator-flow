from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

from config import JWT_ACCESS_TOKEN_EXPIRY_MINUTES, JWT_SECRET, JWT_ALGORITHM
from db.database import get_session
from user.models import DataToken, User

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, JWT_ALGORITHM)

    return encoded_jwt


def verify_token_access(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = DataToken(id=user_id)

    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    token_data = verify_token_access(token)

    user = session.exec(select(User).where(User.id == token_data.id)).first()

    if user is None:
        raise credentials_exception

    return user
