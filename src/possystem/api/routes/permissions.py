from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.permissions.orm import Permission
from typing import Annotated
from sqlalchemy.orm import Session
from ...models.permissions.schemas import PermissionCreate, PermissionUpdate, PermissionResponse, PermissionWithRoles
from ...db.session import get_db  # Use the shared one
from ...utils.permissions import CAN_READ_PERMISSIONS, CAN_CREATE_PERMISSIONS, CAN_UPDATE_PERMISSIONS, CAN_DELETE_PERMISSIONS

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

# user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/',
            response_model=list[PermissionResponse],
            summary="List all permissions",
            description="Retrieve all permissions currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PERMISSIONS
            )
async def read_all(db: db_dependency):
    permissions = db.query(Permission).order_by(Permission.id.asc()).all()
    return permissions


@router.post('/',
            status_code=status.HTTP_201_CREATED,
            response_model=PermissionResponse,
            summary="Create a new permission",
            description="Adds a new permission to the database. The permission name must be unique.",
            dependencies=CAN_CREATE_PERMISSIONS)
async def create_permission(db: db_dependency, permission_request: PermissionCreate):
    existing = db.query(Permission).filter(Permission.name.ilike(permission_request.name)).first()
    if existing:
        raise HTTPException(status_code=409, detail='Permission already exists')
    permission = Permission(**permission_request.model_dump())
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

@router.put('/{permission_id}',
            status_code=status.HTTP_200_OK,
            response_model=PermissionResponse,
            summary="Update an existing permission",
            description="Updates the details of an existing permission by ID. Only the name can be updated.",
            dependencies=CAN_UPDATE_PERMISSIONS)
async def update_permission(permission_id: int, db: db_dependency, permission_request: PermissionUpdate):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()

    if not permission:
        raise HTTPException(status_code=404, detail='Permission not found')

    if permission_request.name:
        existing_permission = db.query(Permission).filter(Permission.name.ilike(permission_request.name)).first()
        if existing_permission and existing_permission.id != permission_id:
            raise HTTPException(status_code=409, detail='Permission name already exists')

    for key, value in permission_request.model_dump(exclude_unset=True).items():
        setattr(permission, key, value)

    db.commit()
    db.refresh(permission)
    return permission

@router.delete('/{permission_id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Delete a permission",
            description="Deletes a permission by ID. This will remove the permission from the database.",
            dependencies=CAN_DELETE_PERMISSIONS)
async def delete_permission(permission_id: int, db: db_dependency):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()

    if not permission:
        raise HTTPException(status_code=404, detail='Permission not found')

    db.delete(permission)
    db.commit()
