from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.product_warehouses.orm import ProductWarehouse
from ...models.products.orm import Product
from ...models.warehouses.orm import Warehouse
from ...models.units.orm import Unit
from ...models.product_warehouses.schemas import ProductWarehouseCreate, ProductWarehouseResponse, ProductWarehouseUpdate, ProductWarehouseSearchParams, ProductWarehouseDetailsResponse
from ...utils.permissions import CAN_READ_PRODUCT_WAREHOUSES, CAN_CREATE_PRODUCT_WAREHOUSES, CAN_UPDATE_PRODUCT_WAREHOUSES, CAN_DELETE_PRODUCT_WAREHOUSES
from datetime import datetime, timezone

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/productswarehouses",
    tags=["Products Warehouses"]
)

@router.get("/",
            response_model=list[ProductWarehouseResponse],
            summary="List all product warehouses",
            description="Retrieve all product warehouses currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCT_WAREHOUSES
            )
async def read_all(db: db_dependency):
    product_warehouses = db.query(ProductWarehouse).all()
    return product_warehouses

