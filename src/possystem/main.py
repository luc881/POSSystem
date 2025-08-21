from fastapi import FastAPI
from .api.routes import permissions, roles, users, branches, auth, units, warehouses, product_categories, products, product_warehouses, product_wallets

app = FastAPI()

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
app.include_router(product_warehouses.router)
app.include_router(product_wallets.router)