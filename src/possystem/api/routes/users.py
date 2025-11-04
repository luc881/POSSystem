from fastapi import Depends, HTTPException, APIRouter, Query
from starlette import status
from ...models.users.orm import User
from typing import Annotated
from sqlalchemy.orm import Session
from ...models.users.schemas import UserResponse, UserCreate, UserUpdate, UserDetailsResponse, UserSearchParams
from ...models.branches.orm import Branch
from ...models.roles.orm import Role
from ...db.session import get_db
from passlib.context import CryptContext
from ...utils.permissions import CAN_READ_USERS, CAN_CREATE_USERS, CAN_UPDATE_USERS, CAN_DELETE_USERS

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get('/',
            response_model=list[UserResponse],
            summary="List all users",
            description="Retrieve all users currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_USERS
            )
async def read_all(db: db_dependency):
    users = db.query(User).all()
    return users


@router.get(
    "/search",
    response_model=list[UserResponse],
    summary="Search users",
    description="Search users by various filters.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_USERS
)
async def search_users(
    db: db_dependency,
    filters: UserSearchParams = Depends()
):
    # Revisión manual si no hay filtros válidos
    if not any(getattr(filters, f) for f in type(filters).model_fields):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe especificar al menos un filtro para la búsqueda"
        )

    query = db.query(User)

    if filters.name:
        query = query.filter(User.name.ilike(f"%{filters.name}%"))
    if filters.surname:
        query = query.filter(User.surname.ilike(f"%{filters.surname}%"))
    if filters.email:
        query = query.filter(User.email.ilike(f"%{filters.email}%"))
    if filters.branch_id:
        query = query.filter(User.branch_id == filters.branch_id)
    if filters.role_id:
        query = query.filter(User.role_id == filters.role_id)
    if filters.phone:
        query = query.filter(User.phone.ilike(f"%{filters.phone}%"))
    if filters.gender:
        query = query.filter(User.gender == filters.gender)
    if filters.type_document:
        query = query.filter(User.type_document.ilike(f"%{filters.type_document}%"))
    if filters.n_document:
        query = query.filter(User.n_document.ilike(f"%{filters.n_document}%"))

    return query.all()


@router.get('/{user_id}',
            response_model=UserResponse,
            summary="Get user by ID",
            description="Retrieve a user by their unique ID.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_USERS
            )
async def read_user_by_id(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/{user_id}/details",
            response_model=UserDetailsResponse,
            summary="Get detailed user info",
            description="Retrieve user along with role, permissions, and branch.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_USERS)
async def read_user_details(user_id: int, db: db_dependency):
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
            status_code=status.HTTP_201_CREATED,
            dependencies = CAN_CREATE_USERS)
async def create_user(user: UserCreate, db: db_dependency):

    plain_password = user.password.get_secret_value()
    user.password = bcrypt_context.hash(plain_password)

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
    if user.role_id is not None:
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

    user_data = user.model_dump()
    user_data["avatar"] = str(user_data["avatar"]) if user_data.get("avatar") else None
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put('/{user_id}',
            response_model=UserResponse,
            summary="Update a user",
            description="Update an existing user's details by their ID.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_UPDATE_USERS)
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

    if user.role_id is not None:
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

    # 👇 Solo campos enviados
    user_data = user.model_dump(exclude_unset=True)

    if "avatar" in user_data:
        user_data["avatar"] = str(user_data["avatar"]) if user_data["avatar"] else None

    for key, value in user_data.items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)

    return existing_user



@router.delete('/{user_id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Delete a user",
            description="Delete an existing user by their ID.",
            dependencies=CAN_DELETE_USERS)
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