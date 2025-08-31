from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone
from ...models.sale_details_attentions.schemas import SaleDetailAttentionResponse, SaleDetailAttentionCreate, SaleDetailAttentionUpdate, SaleDetailAttentionWithRelations
from ...models.sale_details_attentions.orm import SaleDetailAttention
from ...utils.permissions import CAN_READ_SALE_DETAIL_ATTENTIONS, CAN_CREATE_SALE_DETAIL_ATTENTIONS, CAN_UPDATE_SALE_DETAIL_ATTENTIONS, CAN_DELETE_SALE_DETAIL_ATTENTIONS

from ...models.warehouses.orm import Warehouse
from ...models.products.orm import Product
from ...models.units.orm import Unit
from ...models.sale_details.orm import SaleDetail

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/saledetailattentions",
    tags=["Sale Detail Attentions"]
)

@router.get(
    "/",
    response_model=list[SaleDetailAttentionResponse],
    summary="List all sale detail attentions",
    description="Retrieve all sale detail attentions currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_SALE_DETAIL_ATTENTIONS
)
async def read_all(db: db_dependency):
    sale_detail_attentions = db.query(SaleDetailAttention).all()
    return sale_detail_attentions

