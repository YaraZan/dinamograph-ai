import os
from app.api.requests.user_create_request import UserCreate
from app.api.requests.dinamogramm_get_request import DinamogrammGetRequest
from app.api.requests.dinamogramm_mark_request import DinamogrammMarkRequest
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from app.database.database import SessionLocal
from converter.converter import get_random_unmarked_dinamogram
from converter.converter import mark_dinamogramm
from app.controllers.auth.register import register_user
from app.controllers.api.key import validate_api_key

app = FastAPI()

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

@app.get("/d")
async def get_unmarked_dinamogram(request: DinamogrammGetRequest):

    validate_api_key(request.api_key)

    response = get_random_unmarked_dinamogram(request.public_id)
    if os.path.exists(response['url']) and response is not None:
        return {"data": response, "message": "Успешно"} #FileResponse(filename, media_type="image/png", filename="dinamogram.png")
    else:
        return HTTPException(status_code=404, detail="Динамограмма не найдена")

@app.post("/d")
async def mark_dinamogram(request: DinamogrammMarkRequest):

    validate_api_key(request.api_key)

    try:
        mark_dinamogramm(
            id=request.id,
            marker_id=request.marker_id
        )

        return {"data": [], "message": "Успешно маркировано"}
    except Exception:
        return HTTPException(status_code=404, detail="Возникла ошибка")

