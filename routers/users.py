from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, crud, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/", response_model=schemas.UserRead)
def create_user(user_data : schemas.UserCreate, db : Session = Depends(database.get_db)):
    user = crud.create_user(db=db, user_data=user_data)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exists!!!")

@router.get("/{username}", response_model=schemas.UserRead)
def get_user(username : str, db : Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db = db, username = username)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")