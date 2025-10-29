from sqlalchemy.orm import Session
from possystem.models.permissions.orm import Permission
from possystem.db.session import SessionLocal


# --- Lista de permisos a crear ---
PERMISSIONS = [
    # Users
    "users.read", "users.create", "users.update", "users.delete",

    # Branches
    "branches.read", "branches.create", "branches.update", "branches.delete",

    # Permissions
    "permissions.read", "permissions.create", "permissions.update", "permissions.delete",

    # Roles
    "roles.read", "roles.create", "roles.update", "roles.delete",

    # Units
    "units.read", "units.create", "units.update", "units.delete",

    # Warehouses
    "warehouses.read", "warehouses.create", "warehouses.update", "warehouses.delete",

    # Products
    "products.read", "products.create", "products.update", "products.delete",

    # Product categories
    "productscategories.read", "productscategories.create", "productscategories.update", "productscategories.delete",

    # Product warehouses
    "productwarehouses.read", "productwarehouses.create", "productwarehouses.update", "productwarehouses.delete",

    # Product wallets
    "productwallets.read", "productwallets.create", "productwallets.update", "productwallets.delete",

    # Product stock initials
    "productstockinitials.read", "productstockinitials.create", "productstockinitials.update", "productstockinitials.delete",

    # Clients
    "clients.read", "clients.create", "clients.update", "clients.delete",

    # Sales
    "sales.read", "sales.create", "sales.update", "sales.delete",

    # Sale payments
    "salepayments.read", "salepayments.create", "salepayments.update", "salepayments.delete",

    # Sale details
    "saledetails.read", "saledetails.create", "saledetails.update", "saledetails.delete",

    # Sale detail attentions
    "saledetailattentions.read", "saledetailattentions.create", "saledetailattentions.update", "saledetailattentions.delete",

    # Refund products
    "refundproducts.read", "refundproducts.create", "refundproducts.update", "refundproducts.delete",

    # Suppliers
    "suppliers.read", "suppliers.create", "suppliers.update", "suppliers.delete",

    # Purchases
    "purchases.read", "purchases.create", "purchases.update", "purchases.delete",

    # Purchase details
    "purchasedetails.read", "purchasedetails.create", "purchasedetails.update", "purchasedetails.delete",

    # Transports
    "transports.read", "transports.create", "transports.update", "transports.delete",

    # Conversions
    "conversions.read", "conversions.create", "conversions.update", "conversions.delete",

    # Product batches
    "productbatches.read", "productbatches.create", "productbatches.update", "productbatches.delete",
]


def seed_permissions(db: Session):
    """Agrega permisos base a la base de datos, sin duplicar los existentes."""
    created_count = 0

    for perm_name in PERMISSIONS:
        exists = db.query(Permission).filter_by(name=perm_name).first()
        if not exists:
            permission = Permission(name=perm_name)
            db.add(permission)
            created_count += 1

    db.commit()
    print(f"✅ Seeding completado: {created_count} nuevos permisos creados.")


if __name__ == "__main__":
    # Crea una sesión manual para ejecutar el seeding
    db = SessionLocal()
    try:
        seed_permissions(db)
    finally:
        db.close()
