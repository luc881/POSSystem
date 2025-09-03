# from fastapi import Depends, HTTPException, APIRouter
# from typing import Annotated
# from sqlalchemy.orm import Session
# from ...db.session import get_db
# from starlette import status
# from datetime import datetime, timezone
#
# from ...models import Transport
# from ...models.transports.schemas import TransportCreate, TransportUpdate, TransportResponse
# from ...utils.permissions import CAN_READ_TRANSPORTS, CAN_CREATE_TRANSPORTS, CAN_UPDATE_TRANSPORTS, CAN_DELETE_TRANSPORTS
#
# from ...models.users.orm import User
# from ...models.warehouses.orm import Warehouse
#
#
# db_dependency = Annotated[Session, Depends(get_db)]
#
# router = APIRouter(
#     prefix="/transports",
#     tags=["Transports"]
# )
#
# # @router.get(
# #     "/",
# #     response_model=list[TransportResponse],
# #     summary="List all transports",
# #     description="Retrieve all transports currently stored in the database.",
# #     status_code=status.HTTP_200_OK,
# #     dependencies=CAN_READ_TRANSPORTS
# # )
# # async def read_all(db: db_dependency):
# #     transports = db.query(Transport).all()
# #     return transports