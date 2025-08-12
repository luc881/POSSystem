from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from ...models.branches.orm import Branch  # Import Branch ORM
from typing import Annotated
from sqlalchemy.orm import Session
from ...models.branches.schemas import BranchResponse, BranchBase, BranchUpdate # Import UserResponse schema
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

@router.post('/',
            status_code=status.HTTP_201_CREATED,
            response_model=BranchResponse,
            summary="Create a new branch",
            description="Adds a new branch to the database. The branch name must be unique.")
async def create_branch(db: db_dependency, branch_request: BranchBase):
    branch_model = Branch(**branch_request.model_dump())

    branch_found = db.query(Branch).filter(Branch.name.ilike(branch_model.name)).first()

    if branch_found:
        raise HTTPException(status_code=409, detail='Branch already exists')

    db.add(branch_model)
    db.commit()
    db.refresh(branch_model)
    return branch_model

@router.put('/{branch_id}',
            status_code=status.HTTP_200_OK,
            response_model=BranchResponse,
            summary="Update a branch",
            description="Updates an existing branch in the database.")
async def update_branch(branch_id: int, db: db_dependency, branch_request: BranchUpdate):
    branch_model = db.query(Branch).filter(Branch.id == branch_id).first()

    if not branch_model:
        raise HTTPException(status_code=404, detail='Branch not found')

    for key, value in branch_request.model_dump(exclude_unset=True).items():
        setattr(branch_model, key, value)

    db.commit()
    db.refresh(branch_model)
    return branch_model

