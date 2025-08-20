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

