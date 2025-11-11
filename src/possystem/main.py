from fastapi import FastAPI
from .db.session import Base, engine
from contextlib import asynccontextmanager
from .api.routes import permissions, roles, users, branches, auth, units, warehouses, product_categories, products, sales, sale_payments, sale_details, sale_detail_attentions, refund_products, suppliers, purchases, purchase_details, conversions, product_batch

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    # Optionally drop all tables (useful during development)
    print("🔧 Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    print("🔧 Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)

    # Optionally, you could call your init_db seeding function here
    from .seeds.init_db import init_db
    init_db()

    yield  # Everything after this is shutdown code

    # Shutdown code (if needed)
    print("🛑 Application shutdown")

app = FastAPI(lifespan=lifespan)

@app.get('/', tags=["Root"])
def root():
    """Root endpoint."""
    return {"message": "Welcome to the POS System API"}

@app.get('/healthcheck', tags=["Health Check"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "API is running"}

app.include_router(auth.router)
app.include_router(permissions.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(branches.router)
app.include_router(units.router)
app.include_router(warehouses.router)
app.include_router(products.router)
app.include_router(product_categories.router)
app.include_router(sales.router)
app.include_router(sale_payments.router)
app.include_router(sale_details.router)
app.include_router(sale_detail_attentions.router)
app.include_router(refund_products.router)
app.include_router(suppliers.router)
app.include_router(purchases.router)
app.include_router(purchase_details.router)
app.include_router(conversions.router)
app.include_router(product_batch.router)