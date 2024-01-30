from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional

from fastapi import UploadFile, File, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ai.core.dinamograph import create_model, predict
from ai.helpers.data_helper import DataHelper
from database.database import MainSession
from database.models import Marker
from database.models.ai_marker import AIMarker
from database.models.ai_model import AIModel
from schemas.ai import AIModelGetAllResponse, AIModelResponse, AIModelCreateRequest, AIModelUpdateRequest
from service.meta.ai_service_meta import AIServiceMeta

# Main app database instance
db = MainSession()

# DataHelper instance
data_helper = DataHelper()


class AIService(AIServiceMeta):
    def get_all_models(self) -> AIModelGetAllResponse:
        try:
            ai_models = db.query(AIModel).all()

            models = []

            for model in ai_models:
                models.append(AIModelResponse(
                    name=model.name,
                    public_id=str(model.public_id),
                    created_at=model.created_at,
                    categories_num=model.categories_num,
                    train_amount=model.train_amount,
                ))

            models_response = AIModelGetAllResponse(models=models)

            return models_response
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся получить модели")
        finally:
            db.close()

    def get_model_detail(self, model_public_id: str) -> AIModelResponse:
        try:
            matching_model = db.query(AIModel).filter(
                AIModel.public_id == model_public_id).first()

            if matching_model is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Модели с таким названием не существует"
                )

            return AIModelResponse(
                name=matching_model.name,
                public_id=str(matching_model.public_id),
                created_at=matching_model.created_at,
                categories_num=matching_model.categories_num,
                train_amount=matching_model.train_amount,
            )
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся получить данные о модели")
        finally:
            db.close()

    def create_model(self, create_model_request: AIModelCreateRequest):
        try:
            existing_model = db.query(AIModel).filter(AIModel.name == create_model_request.model_name).first()

            if existing_model is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Модель с таким названием уже существует")

            images, ai_markers = create_model(model_name=create_model_request.model_name, epochs=create_model_request.epochs)

            new_model = AIModel(
                name=create_model_request.model_name,
                categories_num=len(ai_markers),
                train_amount=images
            )
            db.add(new_model)

            for ai_marker in ai_markers:
                matching_marker = db.query(Marker).filter(Marker.id == int(ai_marker)).first()

                if matching_marker is None:
                    HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный маркер для динамограммы")

                new_ai_marker = AIMarker()
                new_ai_marker.marker_id = matching_marker.id
                new_ai_marker.ai_model_id = new_model.id
                db.add(new_ai_marker)

            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся создать модель")
        finally:
            db.close()

    def update_model(self, model_update_request: AIModelUpdateRequest):
        try:
            matching_model = db.query(AIModel).filter(
                AIModel.public_id == model_update_request.model_public_id).first()

            if matching_model is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Модели с таким названием не существует"
                )

            matching_model.name = model_update_request.new_name
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся обновить модель")
        finally:
            db.close()

    def delete_model(self, model_public_id: str):
        try:
            matching_model = db.query(AIModel).filter(
                AIModel.public_id == model_public_id).first()

            if matching_model is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Модели с таким названием не существует"
                )

            db.delete(matching_model)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся удалить модель")
        finally:
            db.close()

    @staticmethod
    async def predict(
            model_name: str,
            is_raw: bool = False,
            image: Optional[UploadFile] = File(None),
            raw: Optional[Dict[Any, Any]] = None,
    ) -> str:
        try:
            matching_model = db.query(AIModel).filter(AIModel.name == model_name).first()

            if matching_model is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Модели с таким названием не существует")

            if is_raw and raw is not None:
                image_bytes = data_helper.create_image_bytes_from_raw(raw['x'], raw['y'])
            else:
                image_bytes = await image.read()

            prediction_index = predict(matching_model.name, image_bytes)

            ai_model_matching_markers = db.query(AIMarker).order_by(AIMarker.marker_id).filter(AIMarker.ai_model == matching_model).all()

            if ai_model_matching_markers is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не найдены маркеры для динамограммы")

            prediction_message_raw = ai_model_matching_markers[prediction_index].original_marker.name

            return str(prediction_message_raw)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся выполнить запрос")
        finally:
            db.close()



