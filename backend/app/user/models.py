from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import AutoString, Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, sa_type=AutoString)
    name: str
    role: str


class UserCreate(UserBase):
    password: str


class UserLogin(SQLModel):
    email: EmailStr
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


class Editor(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(unique=True, foreign_key="user.id")


class Token(SQLModel):
    access_token: str
    token_type: str


class DataToken(SQLModel):
    id: UUID | None = None
