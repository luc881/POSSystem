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


@router.post(
    "/",
    response_model=SaleDetailAttentionResponse,
    summary="Create a new sale detail attention",
    description="Create a new sale detail attention with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_SALE_DETAIL_ATTENTIONS
)
async def create(sale_detail_attention: SaleDetailAttentionCreate, db: db_dependency):
    # Check if the associated sale detail exists
    sale_detail = db.query(SaleDetail).filter(SaleDetail.id == sale_detail_attention.sale_detail_id).first()
    if not sale_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated sale detail not found")

    # Check if the associated product exists
    product = db.query(Product).filter(Product.id == sale_detail_attention.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product not found")

    # Check if the associated warehouse exists
    warehouse = db.query(Warehouse).filter(Warehouse.id == sale_detail_attention.warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated warehouse not found")

    # Check if the associated unit exists
    unit = db.query(Unit).filter(Unit.id == sale_detail_attention.unit_id).first()
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated unit not found")

    new_sale_detail_attention = SaleDetailAttention(**sale_detail_attention.model_dump())
    db.add(new_sale_detail_attention)
    db.commit()
    db.refresh(new_sale_detail_attention)
    return new_sale_detail_attention


@router.put(
    "/{id}",
    response_model=SaleDetailAttentionResponse,
    summary="Update an existing sale detail attention",
    description="Update the details of an existing sale detail attention by its ID.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_UPDATE_SALE_DETAIL_ATTENTIONS
)
async def update(id: int, sale_detail_attention: SaleDetailAttentionUpdate, db: db_dependency):
    existing_attention = db.query(SaleDetailAttention).filter(SaleDetailAttention.id == id).first()
    if not existing_attention:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale detail attention not found")

    # # If updating sale_detail_id, check if the associated sale detail exists
    # if sale_detail_attention.sale_detail_id is not None:
    #     sale_detail = db.query(SaleDetail).filter(SaleDetail.id == sale_detail_attention.sale_detail_id).first()
    #     if not sale_detail:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated sale detail not found")

    # If updating product_id, check if the associated product exists
    if sale_detail_attention.product_id is not None:
        product = db.query(Product).filter(Product.id == sale_detail_attention.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product not found")

    # If updating warehouse_id, check if the associated warehouse exists
    if sale_detail_attention.warehouse_id is not None:
        warehouse = db.query(Warehouse).filter(Warehouse.id == sale_detail_attention.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated warehouse not found")

    # If updating unit_id, check if the associated unit exists
    if sale_detail_attention.unit_id is not None:
        unit = db.query(Unit).filter(Unit.id == sale_detail_attention.unit_id).first()
        if not unit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated unit not found")

    for var, value in vars(sale_detail_attention).items():
        if value is not None:
            setattr(existing_attention, var, value)

    existing_attention.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(existing_attention)
    return existing_attention