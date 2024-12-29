from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'username': 'johndoe',
                'email': 'johndoe@gmail.com',
                'password': '12345password',
                'is_staff': False,
                'is_active': True
            }
        }


class Settings(BaseModel):
    auth_jwt_secret_key: str = os.getenv('JWT_KEY')


class LoginModel(BaseModel):
    username: str
    password: str
