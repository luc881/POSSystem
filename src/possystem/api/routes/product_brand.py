from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...utils.permissions import CAN_READ_PRODUCT_BRANDS, CAN_CREATE_PRODUCT_BRANDS, CAN_UPDATE_PRODUCT_BRANDS, CAN_DELETE_PRODUCT_BRANDS
from ...models.product_brand.orm import ProductBrand
from ...models.product_brand.schemas import ProductBrandCreate, ProductBrandResponse, ProductBrandUpdate

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/productsbrand",
    tags=["Products Brand"]
)

@router.get("/",
            response_model=list[ProductBrandResponse],
            summary="List all product brands",
            description="Retrieve all product brands currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCT_BRANDS)
async def read_all(db: db_dependency):
    product_brands = db.query(ProductBrand).all()
    return product_brands