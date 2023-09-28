from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.schemas.Users import UserCreate
from app.database.schemas.Business import BusinessCreate, Business
from app.database.schemas.ExternalUsers import ExternalUserIn, ExternalUserCreate, ExternalUser
from app.database.Queries import business_query, external_users_query
from app.database.Models import Models
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.auth.OAuth2 import get_current_user
from app.auth.OAuth2 import get_business_user
from . import HTTPErrors, utils as business_utils
from app import utils
router = APIRouter(
    prefix="/business",
    tags=["business"],
)



@router.post("/create", response_model=Business)
async def create_business(businessCreate: BusinessCreate, db: Session = Depends(get_db)):
    # Check if business Name, Email, phone number already exists
    utils.user_exists(table=Models.Users, column=Models.Users.username, check_value=businessCreate.email, exception=HTTPErrors.business_already_exists, db=db)  # check email exists
    utils.user_exists(table=Models.Business, column=Models.Business.name, check_value=businessCreate.name, exception=HTTPErrors.business_already_exists, db=db)  # check name exists   
    utils.user_exists(table=Models.Business, column=Models.Business.phone_no, check_value=businessCreate.phone_no, exception=HTTPErrors.business_already_exists, db=db)  # Check phone_no exists
    
    # Create the business user
    user = UserCreate(username=businessCreate.email, password=businessCreate.password)
    user_dict = utils.create_user_auth(user=user, db=db)
    if businessCreate.type == '/sign-up/advertisers/':
        businessCreate.type = 'advertiser'
    if businessCreate.type == '/sign-up/business/':
        businessCreate.type = 'business'
    print('business type:::')
    print(businessCreate.type)
    # Create the business
    business = business_query.create_business(business=businessCreate, db=db)
  
    # Return the business
    return business

@router.post("/create-users", response_model=ExternalUser)
async def create_external_users(user_data: ExternalUserIn, business: str = Depends(get_business_user), db: Session = Depends(get_db)):
    user_email = business_utils.generate_email(full_name=user_data.name, phone_no=user_data.phone_no, business_name=business.name)
    user_password = business_utils.generate_password(full_name=user_data.name, business_name=business.name)
    
    #? Check if user already exists, or his phone_no already exists
    utils.user_exist(table=Models.Users, column=Models.Users.username, check_value=user_email, exception= HTTPErrors.business_user_already_exists, db=db)
    utils.user_exist(table=Models.ExternalUsers, column=Models.ExternalUsers.phone_no, check_value= user_data.phone_no, exception=HTTPErrors.business_user_already_exists, db=db)

    #! Create the External auth user
    user = UserCreate(username= user_email, password=user_password)
    user_dict = utils.create_user_auth(user=user, db=db)
    
    #! Create business user
    user_data.name = user_data.name.capitalize()
    user_data_in_db = ExternalUserCreate(**user_data.dict(), business_id=business.id, email=user_email)
    user = external_users_query.create_user(user=user_data_in_db, db=db) 
    
    return user

@router.get("/get_user_data/")
async def get_user_data(current_user: Models.Users = Depends(get_current_user), db: Session = Depends(get_db)):
    basic_data_dict = {}
    # Fetch user data from Users table
    user_data = db.query(Models.Users).filter(Models.Users.username == current_user.username).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the user is a Business
    business_data = db.query(Models.Business).filter(Models.Business.email == current_user.username).first()
    if business_data:
        # Convert to dictionary and remove sensitive info
        user_data_dict = business_data.__dict__
        user_data_dict.pop('password', None)
        user_data_dict['Jeknins sudo2'] = 'upload update test'
        return user_data_dict


    # Not needed for what I'm doing 

    # # Check if the user is an Employee
    # employee_data = db.query(Models.Employees).filter(Models.Employees.email == current_user.username).first()
    # if employee_data:
    #     user_data_dict = employee_data.__dict__
    #     return user_data_dict

    # # If none of the above, just return the basic user data
    # basic_data_dict = user_data.__dict__
    # basic_data_dict.pop('password', None)
    return basic_data_dict


# @router.get("/get_user_data/")
# async def get_user_data(current_user: Models.Users = Depends(get_current_user), db: Session = Depends(get_db)):
#     print('gets this far')
#     return {"message": "Endpoint reached"}
