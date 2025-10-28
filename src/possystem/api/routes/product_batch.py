from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.permissions.orm import Permission
from ...utils.permissions import CAN_READ_PRODUCT_BATCHES, CAN_CREATE_PRODUCT_BATCHES, CAN_UPDATE_PRODUCT_BATCHES, CAN_DELETE_PRODUCT_BATCHES
from ...models.product_batch.orm import ProductBatch
from ...models.product_batch.schmas import ProductBatchCreate, ProductBatchResponse, ProductBatchUpdate, ProductBatchDetailsResponse

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/productsbatches",
    tags=["Products Batches"]
)