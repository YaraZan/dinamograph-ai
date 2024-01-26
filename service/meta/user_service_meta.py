from abc import ABC, abstractmethod

from fastapi import Depends

from constants.constants import Constants
from schemas.auth import TokenResponse
from schemas.user import UserRegistrationRequest, UserLoginRequest

# Constants instance
constants = Constants()


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

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def generate_uuid(self) -> str:
        pass

