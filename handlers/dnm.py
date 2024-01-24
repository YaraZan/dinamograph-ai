from fastapi import HTTPException, status

from exceptions.dnm import NoDnmhDataError, NoDnmDataError
from exceptions.marker import InvalidMarkerError
from exceptions.user import InvalidEmailError, UserDoesntExistError, PasswordsMatchError, EmailExistsError
from schemas.auth import TokenResponse
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from schemas.user import UserLoginRequest, UserRegistrationRequest
from service.impl.dnm_service import DnmService
from service.impl.user_service import UserService


def handle_get_random_dnm_exceptions(
        public_id: str,
        dnm_service: DnmService
) -> DnmGetRandomResponse:
    try:
        return dnm_service.get_random_dnm(public_id)
    except UserDoesntExistError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Аккаунта не существует")
    except NoDnmhDataError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Данные динамограмм отсутствуют")
    except NoDnmDataError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Динамограмма пустая")
    except InvalidMarkerError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный маркер для динамограммы")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удаётся загрузить динамограмму")


def handle_mark_dnm_exceptions(
        marking_data: DnmMarkRequest,
        dnm_service: DnmService
):
    try:
        return dnm_service.mark_dnm(marking_data)
    except NoDnmDataError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Динамограмма пустая")
    except InvalidMarkerError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный маркер для динамограммы")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удаётся маркировать динамограмму")