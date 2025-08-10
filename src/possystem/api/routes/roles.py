from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.roles.orm import Role
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import SessionLocal
from ...models.roles.schemas import RoleCreate, RoleResponse, RoleUpdate
# from .auth import get_current_user

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/',
            response_model=list[RoleResponse],
            summary="List all roles",
            description="Retrieve all roles currently stored in the database.",
            status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    roles = db.query(Role).all()
    return roles


@router.post('/',
            status_code=status.HTTP_201_CREATED,
            response_model=RoleResponse,
            summary="Create a new role",
            description="Adds a new role to the database. The role name must be unique.")
async def create_permission(db: db_dependency, role_request: RoleCreate):
    role_model = Role(**role_request.model_dump())

    role_found = db.query(Role).filter(Role.name.ilike(role_model.name)).first()

    if role_found:
        raise HTTPException(status_code=409, detail='Permission already exists')

    db.add(role_model)
    db.commit()
    db.refresh(role_model)
    return role_model

@router.put('/{permission_id}',
            response_model=RoleResponse,
            summary="Update an existing permission",
            description="Updates the details of an existing permission by ID. Only the name can be updated.")
async def update_permission(permission_id: int, db: db_dependency, permission_request: RoleUpdate):
    permission = db.query(Role).filter(Role.id == permission_id).first()

    if not permission:
        raise HTTPException(status_code=404, detail='Role not found')

    if permission_request.name:
        existing_permission = db.query(Role).filter(Role.name.ilike(permission_request.name)).first()
        if existing_permission and existing_permission.id != permission_id:
            raise HTTPException(status_code=409, detail='Role name already exists')

    for key, value in permission_request.model_dump(exclude_unset=True).items():
        setattr(permission, key, value)

    db.commit()
    db.refresh(permission)
    return permission

@router.delete('/{permission_id}',
            status_code=status.HTTP_200_OK,
            summary="Delete a permission",
            description="Deletes a permission by ID. This will remove the permission from the database.")
async def delete_permission(role_id: int, db: db_dependency):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail='Role not found')

    db.delete(role)
    db.commit()
    return {"detail": "Role deleted successfully"}
