from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.product_wallets.orm import ProductWallet
from ...models.product_wallets.schemas import ProductWalletCreate, ProductWalletResponse, ProductWalletUpdate
from ...utils.permissions import CAN_READ_PRODUCT_WALLETS, CAN_CREATE_PRODUCT_WALLETS, CAN_UPDATE_PRODUCT_WALLETS, CAN_DELETE_PRODUCT_WALLETS
from datetime import datetime, timezone
from ...models.products.orm import Product
from ...models.units.orm import Unit
from ...models.branches.orm import Branch

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/productswallets",
    tags=["Products Wallets"],
)

@router.get(
    "/",
    response_model=list[ProductWalletResponse],
    summary="List all product wallets",
    description="Retrieve all product wallets currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_PRODUCT_WALLETS
)
async def read_all(db: db_dependency):
    product_wallets = db.query(ProductWallet).all()
    return product_wallets

