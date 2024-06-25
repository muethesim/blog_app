from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, crud, models, JWTtoken
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)

@router.post("/")
def create_blog(blog_data : schemas.BlogCreate, current_user : Annotated[models.User, Depends(JWTtoken.get_current_user)],db : Session = Depends(database.get_db)):
    blog = crud.create_blog(db = db, blog_data=blog_data, user_id=current_user.id)
    if blog:
        return blog
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something Went Wrong!!!")

@router.get("/user/{username}/")
def get_blog_user(username : str, db : Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db = db, username = username)
    return crud.get_blog_by_user(db = db, user = user)

@router.get("/{id}/")
def get_blog(id : int, db : Session = Depends(database.get_db)):
    blog = crud.get_blog_by_id(db = db, id=id)
    if blog:
        return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested Blog Not Found")

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id : int, current_user : Annotated[models.User, Depends(JWTtoken.get_current_user)], db : Session = Depends(database.get_db)):
    if not crud.delete_blog(db=db, id=id, user_id=current_user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")

@router.put("/{id}/", status_code=status.HTTP_202_ACCEPTED)
def update_post(id : int, update_data : schemas.BlogEdit, current_user : Annotated[models.User, Depends(JWTtoken.get_current_user)], db : Session = Depends(database.get_db)):
    if not crud.update_blog(db=db, id=id, user_id=current_user.id, update_data=update_data):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")
    return {"detail" : "Update Successfull."}