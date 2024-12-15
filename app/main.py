from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import investors

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Ensuring my frontend won't run into CORS errors
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(investors.router, prefix="/api")
