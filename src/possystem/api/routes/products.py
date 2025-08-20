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

@router.post("/",
            response_model=ProductResponse,
            summary="Create a new product",
            description="Create a new product with the provided details.",
            status_code=status.HTTP_201_CREATED,
            dependencies=CAN_CREATE_PRODUCTS)
async def create_product(product: ProductCreate, db: db_dependency):
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists."
        )
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}",
            response_model=ProductResponse,
            summary="Update an existing product",
            description="Update the details of an existing product.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_UPDATE_PRODUCTS)
async def update_product(product_id: int, product: ProductUpdate, db: db_dependency):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    if product.sku and product.sku != existing_product.sku:
        sku_exists = db.query(Product).filter(Product.sku == product.sku).first()
        if sku_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists."
            )
    for key, value in product.model_dump().items():
        setattr(existing_product, key, value)
    db.commit()
    db.refresh(existing_product)
    return existing_product

