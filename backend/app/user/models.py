from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    name: str


class UserCreate(UserBase):
    password: str
    role: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserResponseModel(UserBase):
    id: UUID


class Creator(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    password: str
    youtube_api_key: str | None = Field(default=None)


class CreatorCreate(UserBase):
    password: str


class Editor(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    password: str


class EditorCreate(UserBase):
    password: str
