from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.permissions.orm import Permission
from ...utils.permissions import CAN_READ_PRODUCT_BATCHES, CAN_CREATE_PRODUCT_BATCHES, CAN_UPDATE_PRODUCT_BATCHES, CAN_DELETE_PRODUCT_BATCHES
from ...models.product_batch.orm import ProductBatch
from ...models.product_batch.schmas import ProductBatchCreate, ProductBatchResponse, ProductBatchUpdate, ProductBatchDetailsResponse
from ...models.products.orm import Product


db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/productsbatches",
    tags=["Products Batches"]
)

@router.get("/", response_model=list[ProductBatchResponse],
            summary="List all product batches",
            description="Retrieve all product batches currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCT_BATCHES)
def read_all_product_batches(db: db_dependency):
    product_batches = db.query(ProductBatch).all()
    return product_batches

@router.post("/", response_model=ProductBatchResponse,
             summary="Create a new product batch",
             description="Create a new product batch with the provided details.",
             status_code=status.HTTP_201_CREATED,
             dependencies=CAN_CREATE_PRODUCT_BATCHES)
def create_product_batch(product_batch: ProductBatchCreate, db: db_dependency):
    existing_product = db.query(Product).filter(Product.id == product_batch.product_id).first()
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with the given ID does not exist."
        )
    new_product_batch = ProductBatch(**product_batch.model_dump())
    db.add(new_product_batch)
    db.commit()
    db.refresh(new_product_batch)
    return new_product_batch

