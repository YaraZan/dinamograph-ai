import shutil
from typing import List, Any

from dotenv import load_dotenv
from fastapi import HTTPException, status
from matplotlib import pyplot as plt

from ai.helpers.data_helper import DataHelper
from constants.constants import Constants
from database.database import MainSession, TrafficLightSession
from database.models import Dnm, Marker
from database.trafficlight_models import Dnmh, DnmPoint
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse
from service.meta.dnm_service_meta import DnmServiceMeta

# Create database instances
main_database = MainSession()
trafficLight_database = TrafficLightSession()

# Load environment variables
load_dotenv()

# Constants instance
constants = Constants()

# DataHelper instance
data_helper = DataHelper()


class DnmService(DnmServiceMeta):
    """
        Dnm service class

        Implements DnmServiceMeta class methods.
        Used to get and mark dinamogramms from TrafficLight
        app database.

    """
    def get_random_dnm(self, user_public_id: str) -> DnmGetRandomResponse:
        """
        Get a random unplaced dinamogramm.

        Parameters:
            user_public_id (str): Public id of the requesting user

        Returns:
            DnmGetRandomResponse: A response containing a dnm model data.

        Raises:
            UserDoesntExistError: Raised if user with given public id does not exist.
            NoDnmhDataError: Raised if there's no available dinamogramms in database.
            NoDnmDataError: Raised if given dinamogramm doesn't have any points to display
        """
        # matching_user = trafficLight_database.query(Dnm).filter(Dnm.authored_id == user_public_id).first()
        #
        # if matching_user is None:
        #     raise UserDoesntExistError

        matching_dnm = main_database.query(Dnm).filter(
            (Dnm.authored_id == user_public_id) & (Dnm.marker_id == None)
        ).first()

        if matching_dnm is not None:
            matching_dnm_response = DnmGetRandomResponse(
                dnm_id=matching_dnm.id,
                url=matching_dnm.raw_url
            )
            return matching_dnm_response

        dnmh_data = trafficLight_database.query(Dnmh).all()

        if dnmh_data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Данные динамограмм отсутствуют")

        for dnmh in dnmh_data:
            matching_dnm = main_database.query(Dnm).filter(Dnm.dnmh_id == dnmh.Id).first()

            if matching_dnm is None:
                dnm_data = trafficLight_database.query(DnmPoint).filter(DnmPoint.Dnmh_Id == dnmh.Id).order_by(DnmPoint.P).all()

                if dnm_data is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Динамограмма пустая")

                x_values = [dnm.X for dnm in dnm_data]
                y_values = [dnm.Y for dnm in dnm_data]

                raw_output_filename = f'{constants.STORAGE_DATASETS_RAW}/д_{dnmh.Id}.png'
                clear_output_filename = f'{constants.STORAGE_DATASETS_CLEAR}/д_{dnmh.Id}.png'

                data_helper.create_graph(x_values, y_values, raw_output_filename)
                data_helper.create_graph(x_values, y_values, clear_output_filename, is_colorful=False)

                new_dnm = Dnm(
                    dnmh_id=dnmh.Id,
                    authored_id=user_public_id,
                    raw_url=raw_output_filename,
                    clear_url=clear_output_filename,
                )
                main_database.add(new_dnm)
                main_database.commit()

                matching_dnm_response = DnmGetRandomResponse(
                    dnm_id=new_dnm.id,
                    url=new_dnm.raw_url
                )

                return matching_dnm_response

    def mark_dnm(self, marking_data: DnmMarkRequest):
        """
        Mark a dinamogramm with the given marker.

        Parameters:
            marking_data (DnmMarkRequest): Marker data request model

        Raises:
            NoDnmDataError: Raised if given dinamogramm doesn't have any points to display
            InvalidMarkerError: Raised if given marker doesn't exist
        """
        matching_dnm = main_database.query(Dnm).filter(Dnm.id == marking_data.dnm_id).first()
        matching_marker = main_database.query(Marker).filter(Marker.id == marking_data.marker_id).first()

        if matching_dnm is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Динамограмма пустая")

        if matching_marker is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный маркер для динамограммы")

        if matching_dnm.marker is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Динамограмма уже промаркерована")

        output_filename = f'{constants.STORAGE_DATASETS_READY}/д_{marking_data.dnm_id}_{marking_data.marker_id}.png'

        shutil.copy(matching_dnm.clear_url, output_filename)

        matching_dnm.ready_url = output_filename
        matching_dnm.marker = matching_marker
        main_database.commit()


