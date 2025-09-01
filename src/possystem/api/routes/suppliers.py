from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone

from ...models.suppliers.orm import Supplier
from ...models.suppliers.schemas import SupplierCreate, SupplierResponse, SupplierUpdate
from ...utils.permissions import CAN_READ_SUPPLIERS, CAN_CREATE_SUPPLIERS, CAN_UPDATE_SUPPLIERS, CAN_DELETE_SUPPLIERS

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)

@router.get(
    "/",
    response_model=list[SupplierResponse],
    summary="List all suppliers",
    description="Retrieve all suppliers currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_SUPPLIERS
)
async def read_all(db: db_dependency):
    suppliers = db.query(Supplier).all()
    return suppliers

