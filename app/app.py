from fastapi import FastAPI

from api.v1 import c, user, marker, dnm

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/datasets", StaticFiles(directory="datasets"), name="datasets")

app.include_router(d.router, prefix="/d", tags=["d"])
app.include_router(m.router, prefix="/m", tags=["m"])
app.include_router(c.router, prefix="/c", tags=["m"])
app.include_router(u.router, tags=["u"])

@app.get("/")
def home():
    return {'message': 'home'}
