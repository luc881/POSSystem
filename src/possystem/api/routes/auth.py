from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from starlette import status
from ...utils.security import authenticate_user, create_jwt_token


db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/token")
async def login_user(form_data: auth_dependency, db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    expires_delta = timedelta(minutes=30)
    access_token = create_jwt_token(
        username=user.email,
        user_id=user.id,
        role = user.role.name if user.role else None, # Assuming user has a role attribute
        expires_delta=expires_delta
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Successful login"
    }