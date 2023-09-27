from pydantic import BaseModel
from enum import Enum

class UserType(str, Enum):
    EMPLOYEE = 'employee'
    ADVERTISERS = 'advertiser'
    BUSINESS = 'business'

class LoginForm(BaseModel):
    username: str
    password: str
    user_type: str