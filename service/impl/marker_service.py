from dotenv import load_dotenv
from fastapi import HTTPException, status

from constants.constants import Constants
from database.database import MainSession
from database.models import Marker
from schemas.marker import MarkerGetAllResponse, MarkerResponse
from service.meta.marker_service_meta import MarkerServiceMeta

# Main app database instance
main_database = MainSession()

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
    def get_all_markers(self) -> MarkerGetAllResponse:
        """
        Get all dinamogram categorical markers.

        Returns:
            MarkerGetAllResponse: A response containing a list of markers.

        Raises:
            NoMarkersError: Raised if no markers are found in the database.
        """
        try:
            markers_data = main_database.query(Marker).all()

            markers_arr = []

            for marker in markers_data:
                markers_arr.append(
                    MarkerResponse(
                        id=marker.id,
                        name=marker.name,
                        url=marker.url
                    )
                )

            markers_response = MarkerGetAllResponse(markers=markers_arr)

            return markers_response
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удаётся получить маркеры")

