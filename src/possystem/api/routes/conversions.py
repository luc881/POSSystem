from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone

from ...models.conversions.orm import Conversion
from ...models.conversions.schemas import ConversionResponse, ConversionCreate, ConversionUpdate, ConversionWithRelations
from ...utils.permissions import CAN_READ_CONVERSIONS, CAN_CREATE_CONVERSIONS, CAN_UPDATE_CONVERSIONS, CAN_DELETE_CONVERSIONS

from ...models.warehouses.orm import Warehouse
from ...models.products.orm import Product
from ...models.units.orm import Unit
from ...models.users.orm import User

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/conversions",
    tags=["Conversions"]
)

@router.get(
    "/",
    response_model=list[ConversionResponse],
    summary="List all conversions",
    description="Retrieve all conversions currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_CONVERSIONS
)
async def read_all(db: db_dependency):
    conversions = db.query(Conversion).all()
    return conversions

#