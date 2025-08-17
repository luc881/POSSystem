from fastapi import Depends
from ..utils.security import require_permission


# Permissions for user operations
CAN_READ_USERS = [Depends(require_permission("users.read"))]
CAN_CREATE_USERS = [Depends(require_permission("users.create"))]
CAN_UPDATE_USERS = [Depends(require_permission("users.update"))]
CAN_DELETE_USERS = [Depends(require_permission("users.delete"))]

# Permissions for branch operations
CAN_READ_BRANCHES = [Depends(require_permission("branches.read"))]
CAN_CREATE_BRANCHES = [Depends(require_permission("branches.create"))]
CAN_UPDATE_BRANCHES = [Depends(require_permission("branches.update"))]
CAN_DELETE_BRANCHES = [Depends(require_permission("branches.delete"))]

