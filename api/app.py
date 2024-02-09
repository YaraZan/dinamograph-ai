from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.v1.router import v1_router

# Create FastAPI app
app = FastAPI()

# Add CORS middleware to allow all origins (replace with your frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:8000"],  # Set this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# Include api versions
app.include_router(v1_router)
