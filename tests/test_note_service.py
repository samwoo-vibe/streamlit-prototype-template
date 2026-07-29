from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from samwoo_prototype.schemas.notes import NoteCreate
from samwoo_prototype.services.notes import create_note


class FakeNoteRepository:
    def add(self, data: NoteCreate) -> object:
        return SimpleNamespace(
            id=1,
            title=data.title,
            content=data.content,
            created_at=datetime(2026, 1, 1, tzinfo=UTC),
        )

    def list_all(self) -> list[object]:
        return []


def test_create_note_trims_user_input() -> None:
    note = create_note(FakeNoteRepository(), NoteCreate(title="  테스트  ", content="  내용  "))

    assert note.title == "테스트"
    assert note.content == "내용"


def test_create_note_rejects_whitespace_only_title() -> None:
    with pytest.raises(ValueError, match="제목을 입력하세요"):
        create_note(FakeNoteRepository(), NoteCreate(title="   ", content="내용"))
