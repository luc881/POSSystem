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