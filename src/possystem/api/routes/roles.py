from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.roles.orm import Role
from typing import Annotated
from sqlalchemy.orm import Session
from ...models.roles.schemas import RoleCreate, RoleResponse, RoleUpdate, RoleWithPermissions
from ...models.permissions.orm import Permission
from ...db.session import get_db
from ...utils.permissions import CAN_READ_ROLES, CAN_CREATE_ROLES, CAN_UPDATE_ROLES, CAN_DELETE_ROLES

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
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_ROLES
            )
async def read_all(db: db_dependency):
    roles = db.query(Role).all()
    return roles


@router.get('/permissions',
            response_model=list[RoleWithPermissions],
            summary="List all roles with permissions",
            description="Retrieve all roles along with their associated permissions.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_ROLES
            )
async def read_all_with_permissions(db: db_dependency):
    roles = db.query(Role).all()
    return roles


@router.get('/{role_id}',
            response_model=RoleWithPermissions,
            summary="Get a role by ID",
            description="Retrieve a specific role by its ID, including associated permissions.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_ROLES)
async def read_by_id_with_permissions(role_id: int, db: db_dependency):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail='Role not found')

    return role


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RoleWithPermissions,
    summary="Create a new role with optional permissions",
    description="Adds a new role to the database. The role name must be unique. You can include permission IDs to associate them automatically.",
    dependencies=CAN_CREATE_ROLES
)
async def create_role(db: db_dependency, role_request: RoleCreate):
    # 1. Check if role name already exists (case-insensitive)
    role_found = db.query(Role).filter(Role.name.ilike(role_request.name)).first()
    if role_found:
        raise HTTPException(status_code=409, detail="Role name already exists")

    # 2. Create the Role instance (without permissions yet)
    role_model = Role(name=role_request.name)

    db.add(role_model)
    db.commit()
    db.refresh(role_model)

    # 3. If permission_ids were provided, link them
    if role_request.permission_ids:
        permissions = (
            db.query(Permission)
            .filter(Permission.id.in_(role_request.permission_ids))
            .all()
        )

        if not permissions:
            raise HTTPException(status_code=404, detail="No valid permissions found")

        # Optional: Check for missing IDs (so user gets clearer feedback)
        found_ids = {p.id for p in permissions}
        missing_ids = set(role_request.permission_ids) - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Permissions not found: {list(missing_ids)}"
            )

        # 4. Link permissions in batch
        role_model.permissions.extend(permissions)
        db.commit()
        db.refresh(role_model)

    return role_model


@router.put(
    '/{role_id}',
    status_code=status.HTTP_200_OK,
    response_model=RoleWithPermissions,
    summary="Update an existing role (and optionally its permissions)",
    description="Updates the details of an existing role by ID. You can update the name and optionally reassign permissions.",
    dependencies=CAN_UPDATE_ROLES
)
async def update_role(role_id: int, db: db_dependency, role_request: RoleUpdate):
    # 1. Find the role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # 2. Handle name update
    if role_request.name:
        existing_role = (
            db.query(Role)
            .filter(Role.name.ilike(role_request.name))
            .first()
        )
        if existing_role and existing_role.id != role_id:
            raise HTTPException(status_code=409, detail="Role name already exists")
        role.name = role_request.name

    # 3. Handle permission updates (if provided)
    if role_request.permission_ids is not None:
        # Fetch all permissions matching provided IDs
        permissions = (
            db.query(Permission)
            .filter(Permission.id.in_(role_request.permission_ids))
            .all()
        )

        # If none found
        if not permissions and role_request.permission_ids:
            raise HTTPException(status_code=404, detail="No valid permissions found")

        # Check for missing IDs
        found_ids = {p.id for p in permissions}
        missing_ids = set(role_request.permission_ids) - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Permissions not found: {list(missing_ids)}"
            )

        # Replace the entire permission set (you could change this to extend if desired)
        role.permissions = permissions

    # 4. Commit and return updated role
    db.commit()
    db.refresh(role)
    return role


@router.delete(
    '/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role",
    description="Deletes a role by ID. This will remove the role and its associations from the database.",
    dependencies=CAN_DELETE_ROLES
)
async def delete_role(role_id: int, db: db_dependency):
    # 1. Find the role
    role = db.query(Role).filter(Role.id == role_id).one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # 2. Delete it
    db.delete(role)
    db.commit()


