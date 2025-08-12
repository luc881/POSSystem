from fastapi import FastAPI
from .db.session import engine, Base
# from .api import types, regions, pkmspecies
from .api.routes import permissions, roles, users, branches

app = FastAPI()

# TEMP: Drop and recreate all tables (for dev only!)
Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=["Root"])
def root():
    """Root endpoint."""
    return {"message": "Welcome to the POS System API"}

@app.get('/healthcheck', tags=["Health Check"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "API is running"}

app.include_router(permissions.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(branches.router)

# app.include_router(types.router)
# app.include_router(regions.router)
# app.include_router(pkmspecies.router)

