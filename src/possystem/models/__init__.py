# Import schemas first if you like
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

# --- Import ORM models ---
from .users.orm import User
from .roles.orm import Role
from .permissions.orm import Permission
from .branches.orm import Branch
from .product_categories.orm import ProductCategory
from .warehouses.orm import Warehouse
from .products.orm import Product
from .product_warehouses.orm import ProductWarehouse
from .units.orm import Unit
from .product_wallets.orm import ProductWallet
from .product_stock_initials.orm import ProductStockInitial
from .clients.orm import Client
from .sales.orm import Sale


# when you have all coorect you can try
# # src/possystem/models/__init__.py
# import pkgutil
# import importlib
# from .session import Base  # Your SQLAlchemy declarative base
# from pydantic import BaseModel
#
# # -------------------------------------------------
# # 1️⃣ Automatically import all submodules inside models
# # -------------------------------------------------
# package_name = __name__
#
# for finder, name, ispkg in pkgutil.iter_modules(__path__):
#     full_module_name = f"{package_name}.{name}"
#     module = importlib.import_module(full_module_name)
#
#     # Optional: If the module has an 'orm' submodule, import it too
#     try:
#         importlib.import_module(f"{full_module_name}.orm")
#     except ModuleNotFoundError:
#         pass
#
# # -------------------------------------------------
# # 2️⃣ Rebuild all Pydantic forward references
# # -------------------------------------------------
# for subclass in BaseModel.__subclasses__():
#     try:
#         subclass.model_rebuild()
#     except Exception:
#         # Ignore models that don't have forward references
#         pass
