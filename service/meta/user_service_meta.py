from abc import ABC, abstractmethod

from fastapi import Depends

from schemas.auth import TokenResponse
from schemas.user import UserRegistrationRequest, UserLoginRequest
from service.impl.auth_service import AuthService


class UserServiceMeta(ABC):
    @abstractmethod
    def validate_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def validate_password(self, password: str, confirm_password: str) -> bool:
        pass

    @abstractmethod
    def register_user(
            self,
            user: UserRegistrationRequest
    ) -> TokenResponse:
        pass

    @abstractmethod
    def login_user(
            self,
            user: UserLoginRequest
    ) -> TokenResponse:
        pass

