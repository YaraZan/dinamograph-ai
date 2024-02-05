import os
from typing import List

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from constants.constants import Constants
from database.database import MainSession
from database.models import Marker
from database.models.ai_marker import AIMarker
from database.models.ai_model import AIModel
from schemas.marker import MarkerResponse, CreateMarkerRequest
from service.meta.marker_service_meta import MarkerServiceMeta

# Main app database instance
db = MainSession()

# Load environment variables
load_dotenv()

# Constants instance
constants = Constants()


class MarkerService(MarkerServiceMeta):
    """
        Marker service class

        Implements MarkerServiceMeta class methods.
        Used to interact with dinamogram "Markers"
        for "Dinamograph-AI" datasets markup

    """
    def get_all_markers(self) -> List[MarkerResponse]:
        """
        Get all dinamogram categorical markers.

        Returns:
            MarkerGetAllResponse: A response containing a list of markers.

        Raises:
            NoMarkersError: Raised if no markers are found in the database.
        """
        try:
            markers_data = db.query(Marker).all()

            markers_arr = []

            for marker in markers_data:
                markers_arr.append(
                    MarkerResponse(
                        id=marker.id,
                        name=marker.name,
                        url=marker.url
                    )
                )

            return markers_arr
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся получить маркеры")
        finally:
            db.close()

    def get_markers_by_ai_model(self, model_public_id: str) -> List[MarkerResponse]:
        matching_model = db.query(AIModel).filter(
            AIModel.public_id == model_public_id).first()

        if matching_model is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Модели с таким названием не существует"
            )

        used_markers = []

        matching_markers = db.query(AIMarker).filter(AIMarker.ai_model_id == matching_model.id).all()

        for marker in matching_markers:
            used_markers.append(marker.original_marker)

        return used_markers

    def create_marker(self, create_marker_request: CreateMarkerRequest):
        try:
            preprocessed_name = create_marker_request.name.replace(' ', '_')

            print(preprocessed_name)

            url_path = f"{constants.STORAGE_DATASETS_MARKERS}/{preprocessed_name}.png"

            try:
                with open(url_path, "wb") as file:
                    file.write(create_marker_request.image.file.read())
                    file.close()
            except Exception as e:
                raise HTTPException(detail=f"{e}", status_code=500)

            new_marker = Marker(
                name=create_marker_request.name.join('_'),
                url=url_path
            )
            db.add(new_marker)
            db.commit()

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server: Не удаётся создать маркер, {e}")
        finally:
            db.close()

    def delete_marker(self, marker_id):
        try:
            matching_marker = db.query(Marker).filter_by(id=marker_id).first()

            if not matching_marker:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Маркер не существует")

            file_path = matching_marker.url
            if os.path.exists(file_path):
                os.remove(file_path)

            db.delete(matching_marker)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Server: Не удаётся удалить маркер")
        finally:
            db.close()
