from sqlalchemy.orm import Session
from app.database.database import get_db
from fastapi import Depends, HTTPException, status
from app.database.Models.Models import Users, Employees, Business, ExternalUsers
from app.database.schemas import Services
from fastapi import HTTPException, status


def get_user(username: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    return user    
   
def get_user_type(username: str, user_type: str, db: Session):
    user = None
    if user_type == "business" or user_type == "advertiser":
        user = db.query(Business).filter(Business.email == username).first()
        
        if not user:
            user = db.query(ExternalUsers).filter(ExternalUsers.email == username).first()
            
        if user:
            return user.type  # <- This is the change. Directly access the type attribute.
        
    elif user_type == "employee":
        user = db.query(Employees).filter(Employees.email==username).first()
        
        if user:
            return user_type  # If the user_type provided is EMPLOYEE and you find the user, just return the provided user_type
        
    return None

            
    
def create_user(username: str, password: str, db: Session):
    user = Users(username= username, password= password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_employee(employee: Services.EmployeeCreate, db: Session):
    employee = Employees(
        full_name=employee.full_name,
        email= employee.email,
        phone_no= employee.phone_no,
        address= employee.address
    )
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

