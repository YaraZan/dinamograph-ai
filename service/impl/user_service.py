import re
import uuid
from datetime import timedelta, datetime

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status

from constants.constants import Constants
from database.database import MainSession
from database.models import User, Role
from schemas.auth import TokenResponse
from schemas.role import RoleResponse
from schemas.user import UserRegistrationRequest, UserResponse, UserLoginRequest
from service.impl.token_service import TokenService
from service.meta.user_service_meta import UserServiceMeta

# Main app database instance
db = MainSession()

# Load environment variables
load_dotenv()

# Constants instance
constants = Constants()

# Token service instance
token_service = TokenService()

class UserService(UserServiceMeta):
    """
        User service class

        Implements UserServiceMeta class methods.
        Used to registrate and login users in application.

    """
    def validate_email(self, email: str) -> bool:
        """
        Validate given email.

        Parameters:
            email (str): Email to validate

        Returns:
            bool: A boolean indicating if the email is valid.
        """
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

    def validate_password(self, password: str, confirm_password: str) -> bool:
        """
        Validate if password and it's confirmation matches.

        Parameters:
            password (str): Entered password
            confirm_password (str): Confirmed password

        Returns:
            bool: A boolean indicating if passwords match.
        """
        return password == confirm_password

    def register_user(
            self,
            user: UserRegistrationRequest
    ) -> TokenResponse:
        """
        Register a new user in application.

        Parameters:
            user (UserRegistrationRequest): User registration request

        Returns:
            TokenResponse: A jwt token containing the user information.

        Raises:
            InvalidEmailError: Raise if the provided email is invalid
            PasswordsMatchError: Raise if the provided password is invalid
            EmailExistsError: Raise if the provided email is already registered
        """
        if not self.validate_email(user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат почты")

        if not self.validate_password(user.password, user.confirm_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают")

        if db.query(User).filter(User.email == user.email).first() is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Аккаунт с такой почтой уже зарегистрирован")

        user_role = db.query(Role).filter(Role.name == "user").first()

        new_user = User(
            email=user.email,
            name=user.name,
            password=self.hash_password(user.password),
            role=user_role
        )
        db.add(new_user)
        db.commit()

        new_user_role = RoleResponse(
            id=new_user.role.id,
            name=new_user.role.name
        )

        user_registration_response = UserResponse(
            email=new_user.email,
            name=new_user.name,
            public_id=str(new_user.public_id),
            role=new_user_role,
        )

        token_response = TokenResponse(
            token=token_service.tokenize(user_registration_response.model_dump())
        )

        return token_response

    def login_user(
            self,
            user: UserLoginRequest
    ) -> TokenResponse:
        """
        Login a user in application.

        Parameters:
            user (UserRegistrationRequest): User registration request

        Returns:
            TokenResponse: A jwt token containing the user information.

        Raises:
            InvalidEmailError: Raise if the provided email is invalid
            UserDoesntExistError: Raise if user with provided email doesn't exist
            InvalidPasswordError: Raise if the provided password is invalid
        """
        if not self.validate_email(user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат почты")

        matching_user = db.query(User).filter(User.email == user.email).first()

        if matching_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователя с такой почтой не существует")

        if not self.verify_password(user.password, matching_user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный пароль")

        matching_user_role = RoleResponse(
            id=matching_user.role.id,
            name=matching_user.role.name
        )

        user_logging_response = UserResponse(
            email=matching_user.email,
            name=matching_user.name,
            public_id=str(matching_user.public_id),
            role=matching_user_role,
        )

        token_response = TokenResponse(
            token=token_service.tokenize(user_logging_response.model_dump())
        )

        return token_response

    def hash_password(self, password: str) -> str:
        """
        Hashes the provided password using SHA256 algorithm.

        Parameters:
            password (str): Password to hash

        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verifies the provided password against the provided hashed password.

        Parameters:
            password (str): Given password
            hashed_password (str): The hashed password

        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def generate_uuid(self) -> str:
        """
        Generates a random UUID

        Returns:
            str: Random UUID
        """
        return str(uuid.uuid4())

