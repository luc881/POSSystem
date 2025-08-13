from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.users.orm import User  # Import User ORM
from typing import Annotated
from sqlalchemy.orm import Session
from ...models.users.schemas import UserResponse, UserCreate, UserUpdate  # Import UserResponse schema
from ...models.branches.orm import Branch  # Import Branch ORM

from ...db.session import get_db  # Use the shared one

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/',
            response_model=list[UserResponse],
            summary="List all users",
            description="Retrieve all users currently stored in the database.",
            status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    users = db.query(User).all()
    return users

@router.get('/{user_id}',
            response_model=UserResponse,
            summary="Get user by ID",
            description="Retrieve a user by their unique ID.",
            status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post('/',
            response_model=UserResponse,
            summary="Create a new user",
            description="Create a new user with the provided details.",
            status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):

    existing_user = db.query(User).filter(User.email == user.email).first()


    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    if user.branch_id is not None:
        branch = db.query(Branch).filter(Branch.id == user.branch_id).first()
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put('/{user_id}',
            response_model=UserResponse,
            summary="Update a user",
            description="Update an existing user's details by their ID.",
            status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdate, db: db_dependency):
    existing_user = db.query(User).filter(User.id == user_id).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.branch_id is not None:
        branch = db.query(Branch).filter(Branch.id == user.branch_id).first()
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)

    return existing_user


@router.delete('/{user_id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Delete a user",
            description="Delete an existing user by their ID.")
async def delete_user(user_id: int, db: db_dependency):
    existing_user = db.query(User).filter(User.id == user_id).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(existing_user)
    db.commit()

    return None