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
from POSSystem.src.possystem.models.transports.orm import Transport
from POSSystem.src.possystem.models.users.orm import User
from POSSystem.src.possystem.models.roles.orm import Role
from POSSystem.src.possystem.models.permissions.orm import Permission
from POSSystem.src.possystem.models.branches.orm import Branch
from POSSystem.src.possystem.models.product_categories.orm import ProductCategory
from POSSystem.src.possystem.models.warehouses.orm import Warehouse
from POSSystem.src.possystem.models.products.orm import Product
from POSSystem.src.possystem.models.product_warehouses.orm import ProductWarehouse
from POSSystem.src.possystem.models.units.orm import Unit
from POSSystem.src.possystem.models.product_wallets.orm import ProductWallet
from POSSystem.src.possystem.models.product_stock_initials.orm import ProductStockInitial
from POSSystem.src.possystem.models.clients.orm import Client
from POSSystem.src.possystem.models.sales.orm import Sale
from POSSystem.src.possystem.models.sale_payments.orm import SalePayment
from POSSystem.src.possystem.models.sale_details.orm import SaleDetail
from POSSystem.src.possystem.models.sale_details_attentions.orm import SaleDetailAttention
from POSSystem.src.possystem.models.refund_products.orm import RefundProduct
from POSSystem.src.possystem.models.suppliers.orm import Supplier
from POSSystem.src.possystem.models.purchases.orm import Purchase
from POSSystem.src.possystem.models.purchase_details.orm import PurchaseDetail


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
