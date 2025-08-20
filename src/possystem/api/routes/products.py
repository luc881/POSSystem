from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.products.orm import Product
from ...models.products.schemas import ProductCreate, ProductResponse, ProductUpdate, ProductSearchParams, ProductDetailsResponse
from ...models.permissions.orm import Permission
from ...utils.permissions import CAN_READ_PRODUCTS, CAN_CREATE_PRODUCTS, CAN_UPDATE_PRODUCTS, CAN_DELETE_PRODUCTS

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/",
            response_model=list[ProductResponse],
            summary="List all products",
            description="Retrieve all products currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCTS)
async def read_all(db: db_dependency):
    products = db.query(Product).all()
    return products

