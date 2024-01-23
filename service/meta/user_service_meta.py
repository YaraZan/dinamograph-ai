from abc import ABC, abstractmethod
import re

from schemas.user import UserRegistrationRequest, UserLoginRequest, UserRegistrationResponse, UserLoginResponse
from service.impl.auth_service import AuthService


class UserServiceMeta(ABC):
    """ Validation methods """
    @abstractmethod
    def validate_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def validate_password(self, password: str, confirm_password: str) -> bool:
        pass

    """ Methods called from router """
    @abstractmethod
    def register_user(
            self,
            user: UserRegistrationRequest,
            auth_service: AuthService
    ) -> UserRegistrationResponse:
        pass

    @abstractmethod
    def login_user(
            self,
            user: UserLoginRequest,
            auth_service: AuthService
    ) -> UserLoginResponse:
        pass

