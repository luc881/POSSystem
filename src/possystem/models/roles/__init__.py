from .schemas import *
from .orm import Role

# Resolve forward references
from ..permissions.schemas import PermissionResponse
RoleWithPermissions.model_rebuild()
