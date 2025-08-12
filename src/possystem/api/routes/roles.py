from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.roles.orm import Role
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import SessionLocal
from ...models.roles.schemas import RoleCreate, RoleResponse, RoleUpdate, RolePermissionAssociation, RoleWithPermissions
# from .auth import get_current_user
from ...models.permissions.orm import Permission  # Import Permission ORM
from sqlalchemy.orm import selectinload

from ...db.session import get_db  # Use the shared one

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/',
            response_model=list[RoleResponse],
            summary="List all roles",
            description="Retrieve all roles currently stored in the database.",
            status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    roles = db.query(Role).all()
    return roles

@router.get('/permissions',
            response_model=list[RoleWithPermissions],
            summary="List all roles with permissions",
            description="Retrieve all roles along with their associated permissions.",
            status_code=status.HTTP_200_OK)
async def read_all_with_permissions(db: db_dependency):
    roles = db.query(Role).options(selectinload(Role.permissions)).all()
    return roles

@router.post('/',
            status_code=status.HTTP_201_CREATED,
            response_model=RoleResponse,
            summary="Create a new role",
            description="Adds a new role to the database. The role name must be unique.")
async def create_role(db: db_dependency, role_request: RoleCreate):
    role_model = Role(**role_request.model_dump())

    role_found = db.query(Role).filter(Role.name.ilike(role_model.name)).first()

    if role_found:
        raise HTTPException(status_code=409, detail='Permission already exists')

    db.add(role_model)
    db.commit()
    db.refresh(role_model)
    return role_model
@router.put('/{role_id}',
            status_code=status.HTTP_200_OK,
            response_model=RoleResponse,
            summary="Update an existing role",
            description="Updates the details of an existing role by ID. Only the name can be updated.")
async def update_role(role_id: int, db: db_dependency, role_request: RoleUpdate):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail='Role not found')

    if role_request.name:
        existing_role = db.query(Role).filter(Role.name.ilike(role_request.name)).first()
        if existing_role and existing_role.id != role_id:
            raise HTTPException(status_code=409, detail='Role name already exists')

    for key, value in role_request.model_dump(exclude_unset=True).items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)
    return role

@router.delete('/{role_id}',
            status_code=status.HTTP_200_OK,
            summary="Delete a permission",
            description="Deletes a permission by ID. This will remove the permission from the database.")
async def delete_role(role_id: int, db: db_dependency):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail='Role not found')

    db.delete(role)
    db.commit()
    return {"detail": "Role deleted successfully"}

@router.get('/{role_id}',
            response_model=RoleWithPermissions,
            summary="Get a role by ID",
            description="Retrieve a specific role by its ID, including associated permissions.")
async def read_by_id_with_permissions(role_id: int, db: db_dependency):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail='Role not found')

    return role

@router.post("/{role_id}/permissions",
            status_code=status.HTTP_200_OK,
            response_model=RoleWithPermissions,
            summary="Associate a permission to a role",
            description="Links an existing permission to an existing role.")
async def add_permission_to_role(role_id: int, request: RolePermissionAssociation, db: db_dependency):
    # 1. Find the role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # 2. Find the permission
    permission = db.query(Permission).filter(Permission.id == request.permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    # 3. Check if already associated
    if permission in role.permissions:
        raise HTTPException(status_code=409, detail="Permission already associated with role")

    # 4. Append and commit
    role.permissions.append(permission)
    db.commit()
    db.refresh(role)

    return role

@router.delete("/{role_id}/permissions/{permission_id}",
            status_code=status.HTTP_200_OK,
            summary="Remove a permission from a role",
            description="Unlinks a permission from a role by their IDs.")
async def remove_permission_from_role(role_id: int, permission_id: int, db: db_dependency):
    # 1. Find the role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # 2. Find the permission
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    # 3. Check if associated
    if permission not in role.permissions:
        raise HTTPException(status_code=404, detail="Permission not associated with this role")

    # 4. Remove and commit
    role.permissions.remove(permission)
    db.commit()

    return {"detail": "Permission removed from role successfully"}

