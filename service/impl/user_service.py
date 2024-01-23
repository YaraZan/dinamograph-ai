import re

from dotenv import load_dotenv
from fastapi import Depends

from database.database import MainSession
from database.models import User, Role
from exceptions.user import InvalidEmailError, PasswordsMatchError, EmailExistsError, UserDoesntExistError
from exceptions.auth import InvalidPasswordError
from schemas.role import RoleResponse
from schemas.user import UserRegistrationRequest, UserRegistrationResponse, UserLoginRequest, UserLoginResponse
from service.impl.auth_service import AuthService
from service.meta.user_service_meta import UserServiceMeta

# Create database instance
db = MainSession()

# Load environment variables
load_dotenv()


class UserService(UserServiceMeta):
    """ Validation methods """
    def validate_email(self, email: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

    def validate_password(self, password: str, confirm_password: str) -> bool:
        return password == confirm_password

    """ Methods called from router """
    def register_user(
            self,
            user: UserRegistrationRequest,
            auth_service: AuthService = Depends(AuthService)
    ) -> UserRegistrationResponse:
        # Check if email has invalid format
        if not self.validate_email(user.email):
            raise InvalidEmailError

        # Check if passwords doesn't match
        if not self.validate_password(user.password, user.confirm_password):
            raise PasswordsMatchError

        # Check if user with given email already exists
        if db.query(User).filter(User.email == user.email).first() is not None:
            raise EmailExistsError

        # Default user role
        user_role = db.query(Role).filter(Role.name == "user").first()

        # Creating and adding a new user
        new_user = User(
            email=user.email,
            name=user.name,
            password=auth_service.hash_password(user.password),
            public_id=auth_service.generate_uuid(),
            api_key=auth_service.generate_api_key(),
            role=user_role
        )
        db.add(new_user)

        # Role response instance
        new_user_role = RoleResponse(
            id=new_user.role.id,
            name=new_user.role.name
        )

        # Create and return response
        user_registration_response = UserRegistrationResponse(
            email=new_user.email,
            name=new_user.name,
            public_id=new_user.public_id,
            api_key=new_user.api_key,
            role=new_user_role
        )

        return user_registration_response

    def login_user(
            self,
            user: UserLoginRequest,
            auth_service: AuthService = Depends(AuthService)
    ) -> UserLoginResponse:
        # Check if email has invalid format
        if not self.validate_email(user.email):
            raise InvalidEmailError

        # Try to find user with given email
        matching_user = db.query(User).filter(User.email == user.email).first()

        # Check if user with matching email exists
        if matching_user is None:
            raise UserDoesntExistError

        # Check if entered password matches real
        if not auth_service.verify_password(user.password, matching_user.password):
            raise InvalidPasswordError

        # Role response instance
        matching_user_role = RoleResponse(
            id=matching_user.role.id,
            name=matching_user.role.name
        )

        # Create and return response
        user_logging_response = UserLoginResponse(
            email=matching_user.email,
            name=matching_user.name,
            public_id=matching_user.public_id,
            api_key=matching_user.api_key,
            role=matching_user_role
        )

        return user_logging_response

