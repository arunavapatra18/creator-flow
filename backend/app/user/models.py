from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import AutoString, Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, sa_type=AutoString)
    name: str
    role: str


class UserCreate(UserBase):
    password: str


class UserLogin(SQLModel):
    email: EmailStr = Field(index=True, unique=True, sa_type=AutoString)
    password: str


class UserResponseModel(UserBase):
    id: UUID


class User(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    password: str


class Creator(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(unique=True, foreign_key="user.id")
    youtube_api_key: str | None = Field(default=None)


class CreatorAPIUpdateModel(SQLModel):
    youtube_api_key: str


class UserUpdateModel(SQLModel):
    name: str | None
    email: EmailStr | None
    password: str | None


class GetEditorsResponseModel(SQLModel):
    editors: list[UserResponseModel] | None


class GetCreatorsResponseModel(SQLModel):
    creators: list[UserResponseModel] | None


class DataToken(SQLModel):
    id: UUID | None = None


class Token(SQLModel):
    access_token: str
    token_type: str = Field(default="bearer")
