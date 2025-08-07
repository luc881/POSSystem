from .schemas import *
from .orm import Permission

# Resolve forward references
from ..roles.schemas import RoleResponse
PermissionWithRoles.model_rebuild()
