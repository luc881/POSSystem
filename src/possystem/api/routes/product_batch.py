from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.permissions.orm import Permission
from ...utils.permissions import CAN_READ_PRODUCT_BATCHES, CAN_CREATE_PRODUCT_BATCHES, CAN_UPDATE_PRODUCT_BATCHES, CAN_DELETE_PRODUCT_BATCHES
from ...models.product_batch.orm import ProductBatch
from ...models.product_batch.schemas import ProductBatchCreate, ProductBatchResponse, ProductBatchUpdate, ProductBatchDetailsResponse
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

@router.put("/{product_batch_id}", response_model=ProductBatchResponse,
            summary="Update an existing product batch",
            description="Update the details of an existing product batch.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_UPDATE_PRODUCT_BATCHES)
def update_product_batch(product_batch_id: int, product_batch: ProductBatchUpdate, db: db_dependency):
    existing_product_batch = db.query(ProductBatch).filter(ProductBatch.id == product_batch_id).first()
    if not existing_product_batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product batch not found."
        )

    for key, value in product_batch.model_dump(exclude_unset=True).items():
        setattr(existing_product_batch, key, value)

    db.commit()
    db.refresh(existing_product_batch)
    return existing_product_batch

@router.delete("/{product_batch_id}",
               summary="Delete a product batch",
               description="Delete an existing product batch by its ID.",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=CAN_DELETE_PRODUCT_BATCHES)
def delete_product_batch(product_batch_id: int, db: db_dependency):
    existing_product_batch = db.query(ProductBatch).filter(ProductBatch.id == product_batch_id).first()
    if not existing_product_batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product batch not found."
        )
    db.delete(existing_product_batch)
    db.commit()
    return {"detail": "Product batch deleted successfully"}
