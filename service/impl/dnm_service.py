import shutil
from typing import List, Any

from dotenv import load_dotenv
from matplotlib import pyplot as plt

from database.database import MainSession, TrafficLightSession
from database.models import Dnm, Marker
from database.trafficlight_models import Dnmh
from exceptions.user import UserDoesntExistError
from exceptions.dnm import NoDnmhDataError, NoDnmDataError
from exceptions.marker import InvalidMarkerError
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse
from service.meta.dnm_service_meta import DnmServiceMeta

# Create database instance
main_database = MainSession()
trafficLight_database = TrafficLightSession()

# Load environment variables
load_dotenv()

# Storage constraints
RAW_IMAGES = "storage/datasets/raw"
CLEAR_IMAGES = "storage/datasets/clear"
READY_IMAGES = "storage/datasets/ready"


""" Pyplot handlers """


def create_graph(
        x_values: List[Any],
        y_values: List[Any],
        output_filename: str,
        is_colorful: bool = True
) -> None:
    """ Creates a plot with parameters or black and white version
     for marking dataset returns filename """
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


""" Dnm service class """


class DnmService(DnmServiceMeta):
    """ Methods called from router """
    def get_random_dnm(self, user_public_id: str) -> DnmGetRandomResponse:

        matching_user = main_database.query(Dnm).filter(Dnm.authored_id == user_public_id).first()

        # Check if user exists
        if matching_user is None:
            raise UserDoesntExistError

        matching_dnm = main_database.query(Dnm).filter(Dnm.authored_id == user_public_id).first()

        # Check if user has any unmarked entities signed on him
        if matching_dnm is not None:
            matching_dnm_response = DnmGetRandomResponse(
                dnm_id=matching_dnm.dnmh_id,
                url=matching_dnm.raw_url
            )
            return matching_dnm_response

        # Fetch all Dnmh entities from TrafficLight database
        dnmh_data = trafficLight_database.query(Dnmh).all()

        # Check if there's data in trafficlight database Dnmh table
        if dnmh_data is None:
            raise NoDnmhDataError

        for dnmh in dnmh_data:

            matching_dnm = main_database.query(Dnm).filter(Dnm.dnmh_id == dnmh.Id).first()

            # Check if Dnm placed
            if matching_dnm is None:
                dnm_data = dnmh.dnms

                # Check if there's data in trafficlight database Dnmh table
                if dnm_data is None:
                    raise NoDnmDataError

                # Parse x and y values from Dnm data
                x_values = [dnm.X for dnm in dnm_data]
                y_values = [dnm.Y for dnm in dnm_data]

                # Output filenames
                raw_output_filename = f'{RAW_IMAGES}/д_{dnmh.Id}.png'
                clear_output_filename = f'{CLEAR_IMAGES}/д_{dnmh.Id}.png'

                # Create normal and b&w graphs
                create_graph(x_values, y_values, raw_output_filename)
                create_graph(x_values, y_values, clear_output_filename, is_colorful=False)

                # Creating and adding a new dnm
                new_dnm = Dnm(
                    dnmh_id=dnmh.id,
                    authored_id=user_public_id,
                    raw_url=raw_output_filename,
                    clear_url=clear_output_filename,
                )
                main_database.add(new_dnm)

                matching_dnm_response = DnmGetRandomResponse(
                    dnm_id=new_dnm.id,
                    url=new_dnm.raw_url
                )

                return matching_dnm_response

    def mark_dnm(self, marking_data: DnmMarkRequest) -> None:
        matching_dnm = main_database.query(Dnm).filter(Dnm.id == marking_data.dnm_id).first()
        matching_marker = main_database.query(Marker).filter(Marker.id == marking_data.marker_id).first()

        # Check if there's a matching Dnm
        if matching_dnm is None:
            raise NoDnmDataError

        # Check if there's a matching Marker
        if matching_marker is None:
            raise InvalidMarkerError

        # Create an output filename
        output_filename = f'{READY_IMAGES}/д_{marking_data.dnm_id}_{marking_data.marker.id}.png'

        # Copy file to a `datasets/ready` folder
        shutil.copy(matching_dnm.clear_url, output_filename)

        # Update following record in database
        matching_dnm.ready_url = output_filename
        matching_dnm.marker = matching_marker
        main_database.commit()


