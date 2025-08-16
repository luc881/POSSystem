from fastapi import Depends, HTTPException, APIRouter, Query
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db  # Use the shared one
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ...models.users.orm import User
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from starlette import status

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
oauth2_dependency = Annotated[str, Depends(oauth2_scheme)]
db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

SECRET_KEY = "20e0033a91e824639af6207425e11b647c68c2c613abf94f115014e4495a43f6"
ALGORITHM = "HS256"


def authenticate_user(db, email: str, password: str):
    user_model = db.query(User).filter(User.email == email).first()
    if not user_model or not bcrypt_context.verify(password, user_model.password):
        return False
    return user_model


def create_jwt_token(username:str, user_id:int, role:str, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def decode_jwt_token(token: oauth2_dependency):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise credentials_exception
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise credentials_exception


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