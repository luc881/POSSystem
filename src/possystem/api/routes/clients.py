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
