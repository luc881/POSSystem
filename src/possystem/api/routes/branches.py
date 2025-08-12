from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.branches.orm import Branch  # Import Branch ORM
from typing import Annotated
from sqlalchemy.orm import Session
from ...models.branches.schemas import BranchResponse # Import UserResponse schema
from ...db.session import get_db  # Use the shared one

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)

# user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/',
            response_model=list[BranchResponse],
            summary="List all branches",
            description="Retrieve all branches currently stored in the database.",
            status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    branches = db.query(Branch).all()
    return branches