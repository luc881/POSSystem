from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.clients.orm import Client
from ...models.clients.schemas import ClientCreate, ClientResponse, ClientUpdate
from ...utils.permissions import CAN_READ_CLIENTS, CAN_CREATE_CLIENTS, CAN_UPDATE_CLIENTS, CAN_DELETE_CLIENTS
from datetime import datetime, timezone
from ...models.users.orm import User
from ...models.branches.orm import Branch

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@router.get(
    "/",
    response_model=list[ClientResponse],
    summary="List all clients",
    description="Retrieve all clients currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_CLIENTS
)
async def read_all(db: db_dependency):
    clients = db.query(Client).all()
    return clients

@router.post(
    "/",
    response_model=ClientResponse,
    summary="Create a new client",
    description="Create a new client with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_CLIENTS
)
async def create(
    client: ClientCreate,
    db: db_dependency
):
    # Validate user exists
    if not db.query(User).filter_by(id=client.user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID does not exist.")
    # Validate branch exists
    if not db.query(Branch).filter_by(id=client.branch_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Branch ID does not exist.")

    # Check for existing document number
    existing_client = db.query(Client).filter_by(n_document=client.n_document).first()
    if existing_client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document number already exists.")

    new_client = Client(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@router.put(
    "/{client_id}",
    response_model=ClientResponse,
    summary="Update an existing client",
    description="Update the details of an existing client by its ID.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_UPDATE_CLIENTS)
async def update(
    client_id: int,
    client_update: ClientUpdate,
    db: db_dependency
):
    client = db.query(Client).filter_by(id=client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")

    # If n_document is being updated, check for uniqueness
    if client_update.n_document and client_update.n_document != client.n_document:
        existing_client = db.query(Client).filter_by(n_document=client_update.n_document).first()
        if existing_client:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document number already exists.")

    # If user_id is being updated, validate the new user exists
    if client_update.user_id and client_update.user_id != client.user_id:
        if not db.query(User).filter_by(id=client_update.user_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID does not exist.")

    # If branch_id is being updated, validate the new branch exists
    if client_update.branch_id and client_update.branch_id != client.branch_id:
        if not db.query(Branch).filter_by(id=client_update.branch_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Branch ID does not exist.")

    for key, value in client_update.model_dump(exclude_unset=True).items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client