from fastapi import FastAPI
from app.routers import investors
from app.database import Base, engine

# Initialize the database
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(docs_url=None, redoc_url=None)

# Include routers
app.include_router(investors.router, prefix="/api", tags=["investors"])
