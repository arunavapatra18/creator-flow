from fastapi import HTTPException, status
from sqlmodel import Session, select

from user.models import Creator, CreatorCreate, Editor, EditorCreate
from user.util import generate_password_hash


def register_creator(user: CreatorCreate, session: Session):

    # Check if email already exisits
    email_taken = session.exec(select(Creator).where(Creator.email == user.email))
    if email_taken.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    db_creator = Creator.model_validate(user)

    # Hash password before storing to database
    db_creator.password = generate_password_hash(db_creator.password)

    session.add(db_creator)
    session.commit()
    session.refresh(db_creator)
    return db_creator


def register_editor(user: EditorCreate, session: Session):

    # Check if email already exisits
    email_taken = session.exec(select(Editor).where(Editor.email == user.email))
    if email_taken.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    db_editor = Editor.model_validate(user)

    # Hash password before storing to database
    db_editor.password = generate_password_hash(db_editor.password)

    session.add(db_editor)
    session.commit()
    session.refresh(db_editor)
    return db_editor
