from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from typing import Annotated
from ...db.session import get_db
from passlib.context import CryptContext
from starlette import status
from ...models.units.schemas import UnitBase, UnitCreate, UnitUpdate, UnitResponse, UnitDetailsResponse, UnitSearchParams
from ...models.units.orm import Unit
from ...utils.permissions import CAN_READ_UNITS, CAN_CREATE_UNITS, CAN_UPDATE_UNITS, CAN_DELETE_UNITS


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/units",
    tags=["Units"]
)

@router.get('/',
            response_model=list[UnitResponse],
            summary="List all units",
            description="Retrieve all units currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_UNITS
            )
async def read_all(db: db_dependency):
    units = db.query(Unit).all()
    return units

@router.post('/',
            response_model=UnitResponse,
            summary="Create a new unit",
            description="Create a new unit with the provided details.",
            status_code=status.HTTP_201_CREATED,
            dependencies=CAN_CREATE_UNITS
            )
async def create_unit(unit: UnitCreate, db: db_dependency):
    existing_unit = db.query(Unit).filter(Unit.name == unit.name).first()
    if existing_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unit with this name already exists."
        )

    new_unit = Unit(**unit.model_dump())
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

@router.put('/{unit_id}',
            response_model=UnitResponse,
            summary="Update an existing unit",
            description="Update the details of an existing unit.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_UPDATE_UNITS
            )
async def update_unit(unit_id: int, unit: UnitUpdate, db: db_dependency):
    existing_unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not existing_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found."
        )

    # Check if the name is being changed and if the new name already exists
    if unit.name and unit.name != existing_unit.name:
        name_exists = db.query(Unit).filter(Unit.name == unit.name).first()
        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit with this name already exists."
            )

    for key, value in unit.model_dump(exclude_unset=True).items():
        setattr(existing_unit, key, value)

    db.commit()
    db.refresh(existing_unit)
    return existing_unit

@router.delete('/{unit_id}',
            summary="Delete a unit",
            description="Delete a unit by its ID.",
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=CAN_DELETE_UNITS
            )
async def delete_unit(unit_id: int, db: db_dependency):
    existing_unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not existing_unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found."
        )

    db.delete(existing_unit)
    db.commit()
    return {"detail": "Unit deleted successfully."}