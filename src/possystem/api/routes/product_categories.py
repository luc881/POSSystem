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

@router.post("/",
                response_model=ProductCategoryResponse,
                summary="Create a new product category",
                description="Create a new product category with the provided details.",
                status_code=status.HTTP_201_CREATED,
                dependencies=CAN_CREATE_PRODUCT_CATEGORIES
                )
async def create(product_category: ProductCategoryCreate, db: db_dependency):
    existing_category = db.query(ProductCategory).filter(ProductCategory.name == product_category.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product category with this name already exists."
        )
    new_category = ProductCategory(**product_category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

