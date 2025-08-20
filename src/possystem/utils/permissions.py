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

# Permissions for permission operations
CAN_READ_PERMISSIONS = [Depends(require_permission("permissions.read"))]
CAN_CREATE_PERMISSIONS = [Depends(require_permission("permissions.create"))]
CAN_UPDATE_PERMISSIONS = [Depends(require_permission("permissions.update"))]
CAN_DELETE_PERMISSIONS = [Depends(require_permission("permissions.delete"))]

# Permissions for role operations
CAN_READ_ROLES = [Depends(require_permission("roles.read"))]
CAN_CREATE_ROLES = [Depends(require_permission("roles.create"))]
CAN_UPDATE_ROLES = [Depends(require_permission("roles.update"))]
CAN_DELETE_ROLES = [Depends(require_permission("roles.delete"))]

# Permissions for unit operations
CAN_READ_UNITS = [Depends(require_permission("units.read"))]
CAN_CREATE_UNITS = [Depends(require_permission("units.create"))]
CAN_UPDATE_UNITS = [Depends(require_permission("units.update"))]
CAN_DELETE_UNITS = [Depends(require_permission("units.delete"))]

# Permissions for warehouse operations
CAN_READ_WAREHOUSES = [Depends(require_permission("warehouses.read"))]
CAN_CREATE_WAREHOUSES = [Depends(require_permission("warehouses.create"))]
CAN_UPDATE_WAREHOUSES = [Depends(require_permission("warehouses.update"))]
CAN_DELETE_WAREHOUSES = [Depends(require_permission("warehouses.delete"))]

