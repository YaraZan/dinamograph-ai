import shutil
from typing import List, Any

from dotenv import load_dotenv
from matplotlib import pyplot as plt

from constants.constants import Constants
from database.database import MainSession, TrafficLightSession
from database.models import Dnm, Marker
from database.trafficlight_models import Dnmh
from exceptions.user import UserDoesntExistError
from exceptions.dnm import NoDnmhDataError, NoDnmDataError
from exceptions.marker import InvalidMarkerError
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse
from service.meta.dnm_service_meta import DnmServiceMeta

# Create database instances
main_database = MainSession()
trafficLight_database = TrafficLightSession()

# Load environment variables
load_dotenv()

# Constants instance
constants = Constants()


def create_graph(
        x_values: List[Any],
        y_values: List[Any],
        output_filename: str,
        is_colorful: bool = True
):
    """
    Creates a plot, based on given data and saves it.

    Parameters:
        x_values (str): Dinamogramm's x values
        y_values (str): Dinamogramm's y values
        output_filename (str): Filename to save
        is_colorful (bool): Boolean variable to indicate in what color save image
    """
    if is_colorful:
        plt.plot(x_values, y_values, marker='o', linestyle='-', color='green', label='graph')
        plt.title('Динамограмма')
        plt.xlabel('Длина')
        plt.ylabel('Нагрузка')
        plt.legend()
        plt.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')
        plt.close()
    else:
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
        ax.plot(x_values, y_values, marker='o', linestyle='-', color='black', markersize=1)
        ax.set_facecolor('white')

        ax.set_title('')
        ax.set_xlabel('')
        ax.set_ylabel('')

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_xticks([])
        ax.set_yticks([])

        fig.savefig(output_filename, format='png', dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close()


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

        matching_dnm = main_database.query(Dnm).filter(Dnm.authored_id == user_public_id).first()

        if matching_dnm is not None:
            matching_dnm_response = DnmGetRandomResponse(
                dnm_id=matching_dnm.id,
                url=matching_dnm.raw_url
            )
            return matching_dnm_response

        dnmh_data = trafficLight_database.query(Dnmh).all()

        if dnmh_data is None:
            raise NoDnmhDataError

        for dnmh in dnmh_data:
            matching_dnm = main_database.query(Dnm).filter(Dnm.dnmh_id == dnmh.Id).first()

            if matching_dnm is None:
                dnm_data = dnmh.dnms

                if dnm_data is None:
                    raise NoDnmDataError

                x_values = [dnm.X for dnm in dnm_data]
                y_values = [dnm.Y for dnm in dnm_data]

                raw_output_filename = f'{constants.STORAGE_DATASETS_RAW}/д_{dnmh.Id}.png'
                clear_output_filename = f'{constants.STORAGE_DATASETS_CLEAR}/д_{dnmh.Id}.png'

                create_graph(x_values, y_values, raw_output_filename)
                create_graph(x_values, y_values, clear_output_filename, is_colorful=False)

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
            raise NoDnmDataError

        if matching_marker is None:
            raise InvalidMarkerError

        output_filename = f'{constants.STORAGE_DATASETS_READY}/д_{marking_data.dnm_id}_{marking_data.marker_id}.png'

        shutil.copy(matching_dnm.clear_url, output_filename)

        matching_dnm.ready_url = output_filename
        matching_dnm.marker = matching_marker
        main_database.commit()


