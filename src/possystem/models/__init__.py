from .roles.schemas import RoleWithPermissions, RoleResponse
from .permissions.schemas import PermissionWithRoles, PermissionResponse
from .branches.schemas import BranchWithUsersResponse, BranchResponse
from .users.schemas import UserResponse, UserDetailsResponse

# Resolve forward references
RoleWithPermissions.model_rebuild()
PermissionWithRoles.model_rebuild()
BranchWithUsersResponse.model_rebuild()
BranchResponse.model_rebuild()
UserResponse.model_rebuild()
UserDetailsResponse.model_rebuild()

from .users.orm import User
from .roles.orm import Role
from .permissions.orm import Permission
from .branches.orm import Branch
from .product_categories.orm import ProductCategory
from .warehouses.orm import Warehouse