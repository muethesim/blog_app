from . import models, schemas, auth
from sqlalchemy.orm import Session

def get_user_by_username(db: Session, username : str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user_data : schemas.UserCreate):
    if get_user_by_username(db=db, username=user_data.username):
        return
    
    hashed_password = auth.hash_password(password=user_data.password)
    setattr(user_data, "password", hashed_password)
    user_object = models.User(**user_data.model_dump())
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object

def create_blog(db:Session, blog_data:schemas.BlogCreate, user_id:int):
    blog_object = models.Blog(**blog_data.model_dump(), user=user_id)
    db.add(blog_object)
    db.commit()
    db.refresh(blog_object)
    return blog_object

def get_blog_by_id(db : Session, id : int):
    return db.query(models.Blog).filter(models.Blog.id == id).first()

def get_blog_by_user(db : Session, user : models.User, skip : int = 0, limit : int = 100):
    return db.query(models.Blog).filter(models.Blog.user == user.id).offset(skip).limit(limit).all()

def delete_blog(db : Session, id : int, user_id : int):
    delete_count = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user == user_id).delete(synchronize_session=False)
    db.commit()
    return delete_count

def update_blog(db : Session, id : int, user_id : int, update_data : schemas.BlogEdit):
    update_count = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user == user_id).update(update_data.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return update_count