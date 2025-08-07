from .roles.orm import Role
from .permissions.orm import Permission

from .roles.schemas import RoleWithPermissions, RoleResponse
from .permissions.schemas import PermissionWithRoles, PermissionResponse

# Reconstruir referencias cruzadas
RoleWithPermissions.model_rebuild()
PermissionWithRoles.model_rebuild()
