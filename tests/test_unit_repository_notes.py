import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Note, User, Tag
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate
from src.repository.notes import (
    get_note,
    get_notes,
    create_note,
    remove_note,
    update_note,
    update_status_note,
)


class TestNote(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username="test_user", password="qwerty", confirmed=True)
        self.tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
        self.session = MagicMock(spec=Session)

    async def test_get_notes(self):
        limit = 10
        offset = 0
        notes = [
            Note(
                id=1,
                title="test_title_1",
                description="test_description_1",
                user=self.user,
            ),
            Note(
                id=2,
                title="test_title_2",
                description="test_description_2",
                user=self.user,
            ),
        ]
        mocked_notes = MagicMock()
        mocked_notes.scalars.return_value.all.return_value = notes
        self.session.execute.return_value = mocked_notes
        result = await get_notes(offset, limit, self.user, self.session)
        self.assertEqual(result, notes)

    async def test_create_todo(self):
        body = NoteModel(title="test", description="test note", tags=[1, 2])
        self.session.query().filter().all.return_value = self.tags
        result = await create_note(body=body, user=self.user, db=self.session)
        self.assertIsInstance(result, Note)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertEqual(result.tags, self.tags)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_note(self):
        body = NoteUpdate(
            title="test_title", description="test_description", tags=[1, 2], done=True
        )
        note = Note(id=1, title="test_title", description="test_description")
        self.session.query().filter().first.return_value = note
        self.session.query().filter().all.return_value = self.tags
        result = await update_note(
            note_id=1, body=body, user=self.user, db=self.session
        )
        self.assertEqual(result, note)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)
        self.assertEqual(result.tags, self.tags)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_note_not_found(self):
        body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_note(
            note_id=1, body=body, user=self.user, db=self.session
        )
        self.assertIsNone(result)

    async def test_get_note(self):
        note = Note()
        self.session.query().filter().first.return_value = note
        result = await get_note(note_id=1, user=self.user, db=self.session)
        self.assertEqual(result, note)

    async def test_update_status_note_found(self):
        body = NoteStatusUpdate(done=True)
        note = Note()
        self.session.query().filter().first.return_value = note
        self.session.commit.return_value = None
        result = await update_status_note(
            note_id=1, body=body, user=self.user, db=self.session
        )
        self.assertEqual(result, note)

    async def test_update_status_note_not_found(self):
        body = NoteStatusUpdate(done=True)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_status_note(
            note_id=1, body=body, user=self.user, db=self.session
        )
        self.assertIsNone(result)

    async def test_delete_note(self):
        note = Note(
            id=1, title="test_title", description="test_description", user=self.user
        )
        self.session.query().filter().first.return_value = note
        result = await remove_note(note_id=1, user=self.user, db=self.session)
        self.assertEqual(result, note)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Note)

    async def test_remove_note_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_note(note_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)
