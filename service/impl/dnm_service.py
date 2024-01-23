from typing import List, Any

from dotenv import load_dotenv
from matplotlib import pyplot as plt

from database.database import MainSession, TrafficLightSession
from database.models import Dnm
from exceptions import UserDoesntExistError
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse
from service.meta.dnm_service_meta import DnmServiceMeta

# Create database instance
main_database = MainSession()
trafficLight_database = TrafficLightSession()

# Load environment variables
load_dotenv()


""" Pyplot handlers """


def create_graph(
        x_values: List[Any],
        y_values: List[Any],
        output_filename: str,
        is_colorful: bool = True
) -> str:
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


    def mark_dnm(self, marking_data: DnmMarkRequest) -> None:
        pass
