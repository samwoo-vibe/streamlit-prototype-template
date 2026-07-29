from collections.abc import Sequence
from typing import Protocol

from samwoo_prototype.schemas.notes import NoteCreate, NoteRead


class NoteStore(Protocol):
    def add(self, data: NoteCreate) -> object: ...

    def list_all(self) -> Sequence[object]: ...


def create_note(repository: NoteStore, data: NoteCreate) -> NoteRead:
    normalized = data.model_copy(update={"title": data.title.strip(), "content": data.content.strip()})
    if not normalized.title:
        raise ValueError("제목을 입력하세요.")
    return NoteRead.model_validate(repository.add(normalized))


def list_notes(repository: NoteStore) -> list[NoteRead]:
    return [NoteRead.model_validate(note) for note in repository.list_all()]

