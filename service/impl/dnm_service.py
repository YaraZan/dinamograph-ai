import os
import shutil
from typing import List, Any

from dotenv import load_dotenv
from fastapi import HTTPException, status
from matplotlib import pyplot as plt
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ai.helpers.data_helper import DataHelper
from constants.constants import Constants
from database.database import MainSession, TrafficLightSession
from database.models import Dnm, Marker
from database.trafficlight_models import Dnmh, DnmPoint
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse, DnmResponse
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
    def get_all_dnm(self) -> List[DnmResponse]:
        try:
            dnm_raw = main_database.query(Dnm).all()

            dnm_list = []

            for dnm in dnm_raw:
                query = text('SELECT "name" FROM "users" where "public_id" = :aid')

                matching_author_name = trafficLight_database.execute(query, {'aid': dnm.authored_id}).fetchone()
                matching_marker = main_database.query(Marker).filter(Marker.id == dnm.marker_id).first()

                dnm_list.append(DnmResponse(
                    id=dnm.id,
                    author=matching_author_name[0],
                    marker=matching_marker.name if matching_marker else None,
                    raw_url=dnm.raw_url,
                ))

            return dnm_list

        except SQLAlchemyError as e:
            main_database.rollback()
            trafficLight_database.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server: Не удаётся получить динамограммы, {e}")
        finally:
            main_database.close()
            trafficLight_database.close()

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
        try:
            matching_dnm = main_database.query(Dnm).filter(
                (Dnm.authored_id == user_public_id) & (Dnm.marker_id == None)
            ).first()

            if matching_dnm is not None:
                matching_dnm_response = DnmGetRandomResponse(
                    id=matching_dnm.id,
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
                        id=new_dnm.id,
                        url=new_dnm.raw_url
                    )

                    return matching_dnm_response
        except SQLAlchemyError:
            main_database.rollback()
            trafficLight_database.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся получить динамограмму")
        finally:
            main_database.close()
            trafficLight_database.close()

    def mark_dnm(self, marking_data: List[DnmMarkRequest]):
        """
        Mark a dinamogramm with the given marker.

        Parameters:
            marking_data (DnmMarkRequest): Marker data request model

        Raises:
            NoDnmDataError: Raised if given dinamogramm doesn't have any points to display
            InvalidMarkerError: Raised if given marker doesn't exist
        """
        try:
            for marker_request in marking_data:
                matching_dnm = main_database.query(Dnm).filter(Dnm.id == marker_request.id).first()
                matching_marker = main_database.query(Marker).filter(Marker.id == marker_request.marker_id).first()

                if matching_dnm is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Динамограмма пустая")

                if matching_marker is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный маркер для динамограммы")

                output_filename = f'{constants.STORAGE_DATASETS_READY}/д_{marker_request.id}_{marker_request.marker_id}.png'
                shutil.copy(matching_dnm.clear_url, output_filename)

                if marking_data.index(marker_request) is not 0:
                    new_dnm = Dnm(
                        dnmh_id=matching_dnm.dnmh_id,
                        marker=matching_marker,
                        raw_url=matching_dnm.raw_url,
                        clear_url=matching_dnm.clear_url,
                        ready_url=output_filename,
                        authored_id=matching_dnm.authored_id,
                    )
                    main_database.add(new_dnm)
                else:
                    matching_dnm.ready_url = output_filename
                    matching_dnm.marker = matching_marker

            main_database.commit()
        except SQLAlchemyError:
            main_database.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся промаркеровать динамограмму")
        finally:
            main_database.close()

    def delete_dnm(self, dnm_id: int):
        try:
            matching_dnm = main_database.query(Dnm).filter(Dnm.id == dnm_id).first()

            if matching_dnm is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Динамограмма пустая")

            if matching_dnm.raw_url:
                if os.path.exists(matching_dnm.raw_url):
                    os.remove(matching_dnm.raw_url)

            if matching_dnm.clear_url:
                if os.path.exists(matching_dnm.clear_url):
                    os.remove(matching_dnm.clear_url)

            if matching_dnm.ready_url:
                if os.path.exists(matching_dnm.ready_url):
                    os.remove(matching_dnm.ready_url)

            main_database.delete(matching_dnm)
            main_database.commit()

        except SQLAlchemyError:
            main_database.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server: Не удаётся промаркеровать динамограмму")
        finally:
            main_database.close()


