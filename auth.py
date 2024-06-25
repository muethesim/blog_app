from passlib.context import CryptContext
from . import crud
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def check_password(password, hash):
    return pwd_context.verify(password, hash)

def user_auth(db, username, password):
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No User Found!!!")
    
    if not check_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password!!!")
    
    return user