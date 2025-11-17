from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...utils.permissions import CAN_READ_PRODUCT_MASTERS, CAN_CREATE_PRODUCT_MASTERS, CAN_UPDATE_PRODUCT_MASTERS, CAN_DELETE_PRODUCT_MASTERS
from ...models.product_master.orm import ProductMaster
from ...models.product_master.schemas import ProductMasterCreate, ProductMasterResponse, ProductMasterUpdate

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/productsmaster",
    tags=["Products Master"]
)

@router.get("/",
            response_model=list[ProductMasterResponse],
            summary="List all product masters",
            description="Retrieve all product masters currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCT_MASTERS)
async def read_all(db: db_dependency):
    product_masters = db.query(ProductMaster).all()
    return product_masters