from fastapi import APIRouter, status, Depends
from rest_pizza_delivery.db.db_config import Session, engine, get_session
from rest_pizza_delivery.schemas.schemas import SignUpModel, LoginModel
from rest_pizza_delivery.db.db_models import User
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

load_dotenv()

auth_router = APIRouter(prefix='/auth', tags=['auth'])

# Password Hashing
HASH_SCHEME = os.getenv('HASH_SCHEME', 'bcrypt')
DEPRECATED_SCHEME = os.getenv('DEPRECATED_SCHEME', 'auto')
pwd_context = CryptContext(schemes=[HASH_SCHEME], deprecated=DEPRECATED_SCHEME)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.get('/')
async def qq(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    return {'message': 'auth_router'}


@auth_router.post('/signup', response_model=SignUpModel,
                  status_code=status.HTTP_201_CREATED)
async def sign_up(user: SignUpModel):
    # Check unique user fields
    try:
        with get_session() as session:
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

            return SignUpModel(
                username=new_user.username,
                email=new_user.email,
                password=len(new_user.password) * '*',
                is_staff=new_user.is_staff,
                is_active=new_user.is_active
            )

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Login route
@auth_router.post('/login')
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    try:
        with get_session() as session:
            db_user = session.query(User).filter(User.username == user.username).first()
            if db_user and verify_password(user.password, db_user.password):
                access_token = Authorize.create_access_token(subject=db_user.username)
                refresh_token = Authorize.create_refresh_token(subject=db_user.username)
                response = {
                    'access': access_token,
                    'refresh': refresh_token
                }
                return jsonable_encoder(response)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Invalid username or password.')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Server error.')


# Refreshing tokens
@auth_router.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Please provide a valid refresh token.')
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({'access': access_token})