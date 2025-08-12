from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.users.orm import User  # Import User ORM
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import SessionLocal
from ...models.users.schemas import UserResponse, UserCreate  # Import UserResponse schema
# from .auth import get_current_user
from ...models.permissions.orm import Permission  # Import Permission ORM
from sqlalchemy.orm import selectinload

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

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user