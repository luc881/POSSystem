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

# Permissions for product operations
CAN_READ_PRODUCTS = [Depends(require_permission("products.read"))]
CAN_CREATE_PRODUCTS = [Depends(require_permission("products.create"))]
CAN_UPDATE_PRODUCTS = [Depends(require_permission("products.update"))]
CAN_DELETE_PRODUCTS = [Depends(require_permission("products.delete"))]

# Permissions for product category operations
CAN_READ_PRODUCT_CATEGORIES = [Depends(require_permission("productscategories.read"))]
CAN_CREATE_PRODUCT_CATEGORIES = [Depends(require_permission("productscategories.create"))]
CAN_UPDATE_PRODUCT_CATEGORIES = [Depends(require_permission("productscategories.update"))]
CAN_DELETE_PRODUCT_CATEGORIES = [Depends(require_permission("productscategories.delete"))]

# Permissions for product warehouse operations
CAN_READ_PRODUCT_WAREHOUSES = [Depends(require_permission("productwarehouses.read"))]
CAN_CREATE_PRODUCT_WAREHOUSES = [Depends(require_permission("productwarehouses.create"))]
CAN_UPDATE_PRODUCT_WAREHOUSES = [Depends(require_permission("productwarehouses.update"))]
CAN_DELETE_PRODUCT_WAREHOUSES = [Depends(require_permission("productwarehouses.delete"))]



