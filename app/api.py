from typing import Annotated

from app.requests.user_create_request import UserCreate
from app.requests.dinamogramm_mark_request import DinamogrammMarkRequest
from fastapi import FastAPI, HTTPException, Header
from app.database.database import SessionLocal
from app.converter.converter import get_random_unmarked_dinamogramm
from app.converter.converter import get_dinamogramm_markers
from app.converter.converter import mark_dinamogramm
from app.auth.register import register_user
from app.auth.api_key import validate_api_key
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {'message': 'home'}

@app.post("/register")
async def register(user: UserCreate):
    try:
        result = register_user(user=user)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@app.get("/d/{public_id}")
async def get_unmarked_dinamogram(
        public_id: str,
        x_api_key: Annotated[str | None, Header()] = None
    ):
    validate_api_key(x_api_key)

    response = get_random_unmarked_dinamogramm(public_id)
    if response is not None:
        return {"data": response, "message": "Успешно"} #FileResponse(filename, media_type="image/png", filename="dinamogram.png")
    else:
        return HTTPException(status_code=404, detail="Динамограмма не найдена")

@app.post("/d")
async def mark_dinamogram(
        request: DinamogrammMarkRequest,
        x_api_key: Annotated[str | None, Header()] = None
    ):
    validate_api_key(x_api_key)

    try:
        mark_dinamogramm(
            id=request.id,
            marker_id=request.marker_id
        )

        return {"data": [], "message": "Успешно маркировано"}
    except Exception:
        return HTTPException(status_code=404, detail="Возникла ошибка")

@app.get("/m")
async def get_markers(x_api_key: Annotated[str | None, Header()] = None):
    validate_api_key(x_api_key)

    try:
        response = get_dinamogramm_markers()
        return {"data": response, "message": "Успешно"}
    except Exception:
        return HTTPException(status_code=404, detail="Возникла ошибка")

