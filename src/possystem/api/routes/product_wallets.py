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

@router.post(
    "/",
    response_model=ProductWalletResponse,
    summary="Create a new product wallet",
    description="Create a new product wallet with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_PRODUCT_WALLETS
)
async def create(
    product_wallet: ProductWalletCreate,
    db: db_dependency
):
    # Validate product exists
    if not db.query(Product).filter_by(id=product_wallet.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID does not exist.")
    # Validate unit exists
    if not db.query(Unit).filter_by(id=product_wallet.unit_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unit ID does not exist.")
    # Validate branch exists
    if not db.query(Branch).filter_by(id=product_wallet.branch_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Branch ID does not exist.")


    # Check for existing product-unit-branch-type_client combination
    existing_pw = db.query(ProductWallet).filter_by(
        product_id=product_wallet.product_id,
        unit_id=product_wallet.unit_id,
        branch_id=product_wallet.branch_id,
        type_client=product_wallet.type_client
    ).first()
    if existing_pw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product wallet with the same product, unit, branch, and client type already exists.")

    new_product_wallet = ProductWallet(**product_wallet.model_dump())
    db.add(new_product_wallet)
    db.commit()
    db.refresh(new_product_wallet)
    return new_product_wallet