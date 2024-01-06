from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import TagModel, TagResponse
from src.repository import tags as repository_tags
from src.services.auth import auth_service
from src.database.models import User

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagResponse])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_tags function returns a list of tags.

    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A list of tags
    """
    tags = await repository_tags.get_tags(skip, limit, current_user, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The read_tag function is used to retrieve a single tag from the database.
    It takes in an integer representing the ID of the tag, and returns a Tag object.

    :param tag_id: int: Specify the tag id to be read
    :param db: Session: Pass the database session to the function
    :param current_user: User: Ensure that the user is logged in
    :return: A tag object
    :doc-author: Trelent
    """
    tag = await repository_tags.get_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    body: TagModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_tag function creates a new tag in the database.
        The function takes a TagModel object as input, which is validated by pydantic.
        The function also requires an authenticated user to be passed in via the current_user parameter.

    :param body: TagModel: Validate the body of the request
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: A tagmodel object
    :doc-author: Trelent
    """
    return await repository_tags.create_tag(body, current_user, db)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    body: TagModel,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_tag function updates a tag in the database.
        The function takes three arguments:
            body (TagModel): A TagModel object containing the new values for the tag.
            tag_id (int): An integer representing the ID of an existing tag to be updated.
            db (Session, optional): A SQLAlchemy Session object used to query and update data in a database. Defaults to None, which will cause Depends(get_db) to create one when called by FastAPI's dependency injection system.

    :param body: TagModel: Get the data from the request body and
    :param tag_id: int: Specify the id of the tag to be deleted
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: A tagmodel object
    :doc-author: Trelent
    """
    tag = await repository_tags.update_tag(tag_id, body, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_tag function removes a tag from the database.

    :param tag_id: int: Get the tag id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the user who is currently logged in
    :return: A dict, but the schema is not specified
    :doc-author: Trelent
    """
    tag = await repository_tags.remove_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag
