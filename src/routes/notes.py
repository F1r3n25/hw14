from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate, NoteResponse
from src.repository import notes as repository_notes
from src.services.auth import auth_service
from src.database.models import User

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get(
    "/",
    response_model=List[NoteResponse],
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def read_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_notes function returns a list of notes.

    :param skip: int: Skip a certain number of notes
    :param limit: int: Limit the number of notes returned
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :param: Determine the number of notes to skip
    :return: A list of notes
    """
    notes = await repository_notes.get_notes(skip, limit, current_user, db)
    return notes


# previous below


@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_note function is a GET endpoint that returns the note with the given ID.
    It requires authentication and authorization, so it uses auth_service to get the current user.
    If no such note exists, it raises an HTTPException with status code 404 (Not Found).

    :param note_id: int: Specify the note id
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A note object, which is defined in the models
    """
    note = await repository_notes.get_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    body: NoteUpdate,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_note function updates a note in the database.

    :param body: NoteUpdate: Pass the data from the request body to the function
    :param note_id: int: Identify the note to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :param: Get the note id from the url
    :return: A note object
    """
    note = await repository_notes.update_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_status_note(
    body: NoteStatusUpdate,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_status_note function updates the status of a note.

    :param body: NoteStatusUpdate: Get the status of the note from the request body
    :param note_id: int: Get the note id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user that is logged in
    :param: Get the note_id from the url
    :return: A note object
    """
    note = await repository_notes.update_status_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def remove_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_note function removes a note from the database.
        It takes in an integer, note_id, and uses it to find the corresponding Note object in the database.
        If no such Note exists, then a 404 error is raised. Otherwise, that Note is removed from the database.

    :param note_id: int: Get the note id from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: The removed note, which is a dict
    """
    note = await repository_notes.remove_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(body: NoteModel, db: Session = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    """
    The create_note function creates a new note in the database.

    :param body: NoteModel: Get the body of the note
    :param db: Session: Get the database session
    :param user: User: Get the current user
    :return: A notemodel object
    """
    note = await repository_notes.create_note(body, user, db)
    return note
