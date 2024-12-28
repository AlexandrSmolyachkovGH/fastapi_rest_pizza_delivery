from fastapi import APIRouter, status
from rest_pizza_delivery.db.db_config import Session, engine
from rest_pizza_delivery.schemas.schemas import SignUpModel
from rest_pizza_delivery.db.db_models import User
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

auth_router = APIRouter(prefix='/auth', tags=['auth'])

session = Session(bind=engine)

# Password Hashing
HASH_SCHEME = os.getenv('HASH_SCHEME', 'bcrypt')
DEPRECATED_SCHEME = os.getenv('DEPRECATED_SCHEME', 'auto')
pwd_context = CryptContext(schemes=[HASH_SCHEME], deprecated=DEPRECATED_SCHEME)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.get('/')
async def qq():
    return {'message': 'auth_router'}


@auth_router.post('/signup', response_model=SignUpModel,
                  status_code=status.HTTP_201_CREATED)
async def sign_up(user: SignUpModel):
    # Check unique user fields
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this email already exists')
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this username already exists')
    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()
    return new_user
