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


@router.put(
    "/{conversion_id}",
    response_model=ConversionResponse,
    summary="Update a conversion",
    description="Update the details of an existing conversion by its ID.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_UPDATE_CONVERSIONS
)
async def update(conversion_id: int, conversion_update: ConversionUpdate, db: db_dependency):
    conversion = db.query(Conversion).filter(Conversion.id == conversion_id).first()
    if not conversion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversion not found")

    if conversion_update.product_id is not None:
        product = db.query(Product).filter(Product.id == conversion_update.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product not found")

    if conversion_update.warehouse_id is not None:
        warehouse = db.query(Warehouse).filter(Warehouse.id == conversion_update.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source warehouse not found")

    if conversion_update.unit_start_id is not None:
        unit_start = db.query(Unit).filter(Unit.id == conversion_update.unit_start_id).first()
        if not unit_start:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Starting unit not found")

    if conversion_update.unit_end_id is not None:
        unit_end = db.query(Unit).filter(Unit.id == conversion_update.unit_end_id).first()
        if not unit_end:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ending unit not found")

    if conversion_update.user_id is not None:
        user = db.query(User).filter(User.id == conversion_update.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated user not found")

    for key, value in conversion_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(conversion, key, value)

    db.commit()
    db.refresh(conversion)
    return conversion