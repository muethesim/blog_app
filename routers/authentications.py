from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, auth, schemas, JWTtoken
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db : Session = Depends(database.get_db)):
    user = auth.user_auth(db=db, username=form_data.username, password=form_data.password)
    access_token = JWTtoken.create_access_token(data={"sub": user.username})
    return schemas.Token(access_token=access_token, token_type="bearer")