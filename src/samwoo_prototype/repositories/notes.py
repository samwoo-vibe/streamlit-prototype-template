from collections.abc import Sequence

from sqlalchemy import select

from samwoo_prototype.database import SessionLocal
from samwoo_prototype.models import Note
from samwoo_prototype.schemas.notes import NoteCreate


class NoteRepository:
    def add(self, data: NoteCreate) -> Note:
        with SessionLocal() as session:
            note = Note(title=data.title, content=data.content)
            session.add(note)
            session.commit()
            session.refresh(note)
            return note

    def list_all(self) -> Sequence[Note]:
        with SessionLocal() as session:
            statement = select(Note).order_by(Note.id.desc()).limit(100)
            return session.scalars(statement).all()
