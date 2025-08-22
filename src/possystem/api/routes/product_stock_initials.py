from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.product_stock_initials.orm import ProductStockInitial
from ...models.product_stock_initials.schemas import ProductStockInitialCreate, ProductStockInitialResponse, ProductStockInitialUpdate
from ...utils.permissions import CAN_READ_PRODUCT_STOCK_INITIALS, CAN_CREATE_PRODUCT_STOCK_INITIALS, CAN_UPDATE_PRODUCT_STOCK_INITIALS, CAN_DELETE_PRODUCT_STOCK_INITIALS
from datetime import datetime, timezone
from ...models.products.orm import Product
from ...models.units.orm import Unit
from ...models.warehouses.orm import Warehouse

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/productstockinitials",
    tags=["Products Stock Initials"]
)

@router.get(
    "/",
    response_model=list[ProductStockInitialResponse],
    summary="List all product stock initials",
    description="Retrieve all product stock initials currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_PRODUCT_STOCK_INITIALS
)
async def read_all(db: db_dependency):
    product_stock_initials = db.query(ProductStockInitial).all()
    return product_stock_initials


