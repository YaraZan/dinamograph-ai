from dotenv import load_dotenv

from constants.constants import Constants
from database.database import MainSession
from database.models import Marker
from exceptions.marker import NoMarkersError
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
        markers_data = main_database.query(Marker).all()

        if markers_data is None:
            raise NoMarkersError

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
