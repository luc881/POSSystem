from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.products.orm import Product
from ...models.products.schemas import ProductCreate, ProductResponse, ProductUpdate, ProductSearchParams, ProductDetailsResponse
from ...utils.permissions import CAN_READ_PRODUCTS, CAN_CREATE_PRODUCTS, CAN_UPDATE_PRODUCTS, CAN_DELETE_PRODUCTS

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/",
            response_model=list[ProductResponse],
            summary="List all products",
            description="Retrieve all products currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCTS)
async def read_all(db: db_dependency):
    products = db.query(Product).all()
    return products

@router.get("/search",
            response_model=list[ProductResponse],
            summary="Search and filter products",
            description="Search products by title, or availability.",
            dependencies=CAN_READ_PRODUCTS)
async def search_products(db: db_dependency, params: ProductSearchParams = Depends()):
    query = db.query(Product)

    if params.title:
        query = query.filter(Product.title.ilike(f"%{params.title}%"))
    if params.is_active is not None:
        query = query.filter(Product.is_active == params.is_active)

    products = query.all()
    return products

@router.get("/{product_id}",
            response_model=ProductDetailsResponse,
            summary="Get product details",
            description="Retrieve detailed information about a specific product by its ID.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCTS)
async def read_product(product_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    return product



@router.post("/",
            response_model=ProductDetailsResponse,
            summary="Create a new product",
            status_code=status.HTTP_201_CREATED,
            dependencies=CAN_CREATE_PRODUCTS)
async def create_product(product_request: ProductCreate, db: db_dependency):

    # 1. Validar SKU duplicado
    existing_product = db.query(Product).filter(Product.sku == product_request.sku).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists."
        )

    # 2. Crear modelo base sin ingredientes
    product_model = Product(
        **product_request.model_dump(mode="json", exclude={"ingredient_ids"})
    )
    db.add(product_model)
    db.commit()
    db.refresh(product_model)

    # 3. Asignar ingredientes si se enviaron
    if product_request.ingredient_ids:
        from possystem.models.ingredients.orm import Ingredient

        ingredients = (
            db.query(Ingredient)
            .filter(Ingredient.id.in_(product_request.ingredient_ids))
            .all()
        )

        if not ingredients:
            raise HTTPException(status_code=404, detail="No valid ingredients found")

        # Checar IDs faltantes (igual que roles)
        found = {i.id for i in ingredients}
        missing = set(product_request.ingredient_ids) - found
        if missing:
            raise HTTPException(
                status_code=404,
                detail=f"Ingredients not found: {list(missing)}"
            )

        # Asignación tipo "role.permissions.extend()"
        product_model.ingredients.extend(ingredients)
        db.commit()
        db.refresh(product_model)

    return product_model


@router.put("/{product_id}",
            response_model=ProductDetailsResponse,
            summary="Update an existing product",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_UPDATE_PRODUCTS)
async def update_product(product_id: int, product_request: ProductUpdate, db: db_dependency):

    # 1. Verificar existe
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    # 2. Validar SKU si cambia
    if product_request.sku and product_request.sku != product.sku:
        sku_exists = db.query(Product).filter(Product.sku == product_request.sku).first()
        if sku_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists."
            )

    # 3. Actualizar campos normales
    for key, value in product_request.model_dump(
            mode="json",  # 👈 NECESARIO
            exclude={"ingredient_ids"},
            exclude_unset=True
    ).items():
        setattr(product, key, value)

    # 4. Actualizar ingredientes si se enviaron
    if product_request.ingredient_ids is not None:
        from possystem.models.ingredients.orm import Ingredient

        ingredients = (
            db.query(Ingredient)
            .filter(Ingredient.id.in_(product_request.ingredient_ids))
            .all()
        )

        if not ingredients and product_request.ingredient_ids:
            raise HTTPException(status_code=404, detail="No valid ingredients found")

        # Buscar faltantes
        found = {i.id for i in ingredients}
        missing = set(product_request.ingredient_ids) - found
        if missing:
            raise HTTPException(
                status_code=404,
                detail=f"Ingredients not found: {list(missing)}"
            )

        # Reemplazar la lista completa (igual que roles)
        product.ingredients = ingredients

    db.commit()
    db.refresh(product)
    return product


@router.patch("/{product_id}/toggle-active",
            response_model=ProductResponse,
            summary="Toggle product availability",
            description="Activate or deactivate a product quickly.",
            dependencies=CAN_UPDATE_PRODUCTS)
async def toggle_product_active(product_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    product.is_active = not product.is_active
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}",
            summary="Delete a product",
            description="Delete a product by its ID.",
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=CAN_DELETE_PRODUCTS)
async def delete_product(product_id: int, db: db_dependency):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    db.delete(existing_product)
    db.commit()
