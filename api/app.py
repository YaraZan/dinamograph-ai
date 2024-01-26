from fastapi import FastAPI
from api.v1.router import v1_router

# Create FastAPI app
app = FastAPI()

# Include api versions
app.include_router(v1_router)
