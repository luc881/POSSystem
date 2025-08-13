from .roles.orm import Role
from .permissions.orm import Permission
from .branches.orm import Branch  # if you have one
from .users.orm import User  # if you have one


from .roles.schemas import RoleWithPermissions, RoleResponse
from .permissions.schemas import PermissionWithRoles, PermissionResponse
from .branches.schemas import BranchWithUsersResponse, BranchResponse
from .users.schemas import UserResponse

# Reconstruir referencias cruzadas
RoleWithPermissions.model_rebuild()
PermissionWithRoles.model_rebuild()
BranchWithUsersResponse.model_rebuild()
UserResponse.model_rebuild()