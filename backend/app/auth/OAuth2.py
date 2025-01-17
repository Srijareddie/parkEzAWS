from fastapi import Cookie, HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .. import config
from datetime import datetime, timedelta
from app.database.Queries import user_query, business_query
from app.database.database import get_db
from app.database.schemas.Users import User
from app.database.schemas.Business import Business
from sqlalchemy.orm import Session
from app.database.schemas import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password Hashing
def hash_password(plain_password):
    return pwd_context.hash(plain_password)

# Password Verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Verify User
def authorize_user(username: str, user_type: str, db: Session) -> bool:
    user = user_query.get_user_type(username= username, user_type=user_type, db=db)
    if user:
        if user == user_type:
            return True
        
    raise HTTPException(status_code=401, detail='Unauthorized User') 
    
# Authenticate User
def authenticate_user(username: str, password: str, user_type: str, db: Session):
    user = user_query.get_user(username= username, db=db)
    
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    authorize_user(username=username, user_type=user_type, db=db)
    
    
    return user 


# Create Access Token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

# validate token
def validate_token(credentials_exception: HTTPException, access_token : str = Cookie("access_token")):
    try:
        payload = jwt.decode(token = access_token, key = config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        token_data = Token.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception

# get current user
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    # Extract the token from the Authorization header
    scheme, _, token = authorization.partition(' ')
    if scheme.lower() != 'bearer':
        raise credentials_exception

    token_data = validate_token(access_token=token, credentials_exception=credentials_exception)
    user = user_query.get_user(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


def get_business_user(access_token: str = Depends(get_current_user), db: Session = Depends(get_db)):
    business_dict = User(**access_token.__dict__)
    business = business_query.get_business_by_email(email=business_dict.username, db=db)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized user"
        )

    business.type = business.type.value
    business_dict = business.__dict__
    business = Business(**business_dict)
    
    return business
    