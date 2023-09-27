from pydantic import BaseModel
from datetime import datetime

class BusinessBase(BaseModel):
    email: str
    name: str
    phone_no: str
    address: str
    type: str
    
class BusinessCreate(BusinessBase):
    password: str
    
class Business(BusinessBase):
    id: int
    date_joined: datetime
    is_active: bool
    
    class Config:
        orm_mode = True

class BusinessUsers(Business):
    pass

    class Config:
        orm_mode = True