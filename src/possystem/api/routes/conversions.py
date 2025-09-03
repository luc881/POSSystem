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

@router.post(
    "/",
    response_model=ConversionResponse,
    summary="Create a new conversion",
    description="Create a new conversion with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_CONVERSIONS
)
async def create(conversion: ConversionCreate, db: db_dependency):
    # Check if the associated warehouses exist
    warehouse = db.query(Warehouse).filter(Warehouse.id == conversion.warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source warehouse not found")

    # Check if the associated product exists
    product = db.query(Product).filter(Product.id == conversion.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product not found")

    # Check if the associated unit exists
    unit_start = db.query(Unit).filter(Unit.id == conversion.unit_start_id).first()
    if not unit_start:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Starting unit not found")

    unit_end = db.query(Unit).filter(Unit.id == conversion.unit_end_id).first()
    if not unit_end:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ending unit not found")

    # Check if the associated user exists
    user = db.query(User).filter(User.id == conversion.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated user not found")

    new_conversion = Conversion(**conversion.model_dump())
    db.add(new_conversion)
    db.commit()
    db.refresh(new_conversion)
    return new_conversion