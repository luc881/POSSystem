from fastapi import Depends
from ..utils.security import require_permission


# Permissions for user operations
CAN_READ_USERS = [Depends(require_permission("users.read"))]
CAN_CREATE_USERS = [Depends(require_permission("users.create"))]
CAN_UPDATE_USERS = [Depends(require_permission("users.update"))]
CAN_DELETE_USERS = [Depends(require_permission("users.delete"))]