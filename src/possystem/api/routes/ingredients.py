from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.ingredients.orm import Ingredient
from ...models.ingredients.schemas import IngredientCreate, IngredientResponse, IngredientUpdate
from ...utils.permissions import CAN_READ_INGREDIENTS, CAN_CREATE_INGREDIENTS, CAN_UPDATE_INGREDIENTS, CAN_DELETE_INGREDIENTS

db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)

@router.get("/",
            response_model=list[IngredientResponse],
            summary="List all ingredients",
            description="Retrieve all ingredients currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_INGREDIENTS)
async def read_all(db: db_dependency):
    ingredients = db.query(Ingredient).all()
    return ingredients

@router.post("/",
             response_model=IngredientResponse,
             summary="Create a new ingredient",
             description="Create a new ingredient with the provided details.",
             status_code=status.HTTP_201_CREATED,
             dependencies=CAN_CREATE_INGREDIENTS)
async def create(ingredient: IngredientCreate, db: db_dependency):

    # chech if ingredient with the same name exists
    existing_ingredient = db.query(Ingredient).filter(Ingredient.name == ingredient.name).first()
    if existing_ingredient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient with this name already exists."
        )

    db_ingredient = Ingredient(**ingredient.model_dump())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

@router.put("/{ingredient_id}",
            response_model=IngredientResponse,
            summary="Update an existing ingredient",
            description="Update the details of an existing ingredient by its ID.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_UPDATE_INGREDIENTS)
async def update(ingredient_id: int, ingredient: IngredientUpdate, db: db_dependency):
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found."
        )

    # Check if updating the name to one that already exists
    if ingredient.name and ingredient.name != db_ingredient.name:
        existing_ingredient = db.query(Ingredient).filter(Ingredient.name == ingredient.name).first()
        if existing_ingredient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient with this name already exists."
            )


    for key, value in ingredient.model_dump(exclude_unset=True).items():
        setattr(db_ingredient, key, value)

    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient