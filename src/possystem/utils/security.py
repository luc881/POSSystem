from fastapi import Depends, HTTPException
from starlette import status
from ..models.users.orm import User
from typing import Annotated
from sqlalchemy.orm import Session
from ..db.session import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
oauth2_dependency = Annotated[str, Depends(oauth2_scheme)]
auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


SECRET_KEY = "20e0033a91e824639af6207425e11b647c68c2c613abf94f115014e4495a43f6"
ALGORITHM = "HS256"


def authenticate_user(db, email: str, password: str):
    user_model = db.query(User).filter(User.email == email).first()
    if not user_model or not bcrypt_context.verify(password, user_model.password):
        return False
    return user_model


def create_jwt_token(username:str, user_id:int, role:str, expires_delta: timedelta): #Get current user data
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


user_dependency = Annotated[dict, Depends(decode_jwt_token)]


def require_permission(permission: str):
    async def checker(
        token_data: user_dependency,
        db: db_dependency
    ):
        # Fetch the user from DB
        user = db.query(User).filter(User.id == token_data["id"]).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

            # Ensure user has a role
        if not user.role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role not assigned")

        # Collect permissions from user's role
        user_permissions = {perm.name for perm in user.role.permissions}  # assuming role.permissions relationship

        # Check required permission
        if permission not in user_permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        return token_data  # so endpoint still knows who the user is
    return checker