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

@router.put(
    "/{product_wallet_id}",
    response_model=ProductWalletResponse,
    summary="Update an existing product wallet",
    description="Update the details of an existing product wallet.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_UPDATE_PRODUCT_WALLETS
)
async def update(
    product_wallet_id: int,
    product_wallet: ProductWalletUpdate,
    db: db_dependency
):
    existing_wallet = db.query(ProductWallet).filter_by(id=product_wallet_id).first()
    if not existing_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product wallet not found.")

    # Validate product exists
    if product_wallet.product_id is not None:
        if not db.query(Product).filter_by(id=product_wallet.product_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID does not exist.")

    # Validate unit exists
    if product_wallet.unit_id is not None:
        if not db.query(Unit).filter_by(id=product_wallet.unit_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unit ID does not exist.")

    # Validate branch exists
    if product_wallet.branch_id is not None:
        if not db.query(Branch).filter_by(id=product_wallet.branch_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Branch ID does not exist.")

    # Check for duplicates (only if keys are being updated)
    if any([
        product_wallet.product_id is not None and product_wallet.product_id != existing_wallet.product_id,
        product_wallet.unit_id is not None and product_wallet.unit_id != existing_wallet.unit_id,
        product_wallet.branch_id is not None and product_wallet.branch_id != existing_wallet.branch_id,
        product_wallet.type_client is not None and product_wallet.type_client != existing_wallet.type_client,
    ]):
        duplicate_check = db.query(ProductWallet).filter_by(
            product_id=product_wallet.product_id,
            unit_id=product_wallet.unit_id,
            branch_id=product_wallet.branch_id,
            type_client=product_wallet.type_client
        ).first()

        if duplicate_check and duplicate_check.id != existing_wallet.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product wallet with the same product, unit, branch, and client type already exists.")

    # Update fields
    for key, value in product_wallet.model_dump(exclude_unset=True).items():
        setattr(existing_wallet, key, value)

    existing_wallet.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(existing_wallet)
    return existing_wallet

@router.delete(
    "/{product_wallet_id}",
    summary="Delete a product wallet",
    description="Delete a product wallet by its ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=CAN_DELETE_PRODUCT_WALLETS
)
async def delete(
    product_wallet_id: int,
    db: db_dependency
):
    product_wallet = db.query(ProductWallet).filter_by(id=product_wallet_id).first()
    if not product_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product wallet not found.")

    # Soft delete by setting deleted_at
    product_wallet.deleted_at = datetime.now(timezone.utc)
    db.commit()

    return {"detail": "Product wallet deleted successfully."}