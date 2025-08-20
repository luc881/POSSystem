from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.product_categories.orm import ProductCategory
from ...models.product_categories.schemas import ProductCategoryCreate, ProductCategoryResponse, ProductCategoryUpdate
from ...utils.permissions import CAN_READ_PRODUCT_CATEGORIES, CAN_CREATE_PRODUCT_CATEGORIES, CAN_UPDATE_PRODUCT_CATEGORIES, CAN_DELETE_PRODUCT_CATEGORIES

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/productscategories",
    tags=["Products Categories"]
)

@router.get("/",
            response_model=list[ProductCategoryResponse],
            summary="List all product categories",
            description="Retrieve all product categories currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCT_CATEGORIES
            )
async def read_all(db: db_dependency):
    product_categories = db.query(ProductCategory).all()
    return product_categories