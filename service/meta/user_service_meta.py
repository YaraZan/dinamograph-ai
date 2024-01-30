from abc import ABC, abstractmethod

from fastapi import Depends

from constants.constants import Constants
from schemas.auth import TokenResponse
from schemas.user import UserRegistrationRequest, UserLoginRequest, UserResponse

# Constants instance
constants = Constants()


class UserServiceMeta(ABC):
    @abstractmethod
    def get_user_details(self, user_public_id: str) -> UserResponse:
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


