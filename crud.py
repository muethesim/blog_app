from . import models, schemas, auth, cache
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

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

def create_blog(db:Session, blog_data:schemas.BlogCreate, user:models.User):
    blog_object = models.Blog(**blog_data.model_dump(), user=user.id)
    db.add(blog_object)
    db.commit()
    db.refresh(blog_object)
    cache.del_cache_blog_by_username(user.username)
    return blog_object

def get_blog_by_id(db : Session, id : int):
    blog = cache.get_cache_blog_by_id(id)
    if blog:
        print("HIT")
        return blog
    print("MISS")
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        blog_dict = jsonable_encoder(schemas.BlogRead.model_validate(blog))
        cache.set_cache_blog_by_id(id, blog_dict)
    return blog

def get_blog_by_user(db : Session, user : models.User, skip : int = 0, limit : int = 100):
    blogs = cache.get_cache_blog_by_username(user.username)
    if blogs:
        print("HIT")
        return blogs
    print("MISS")
    blogs = db.query(models.Blog).filter(models.Blog.user == user.id).offset(skip).limit(limit).all()
    if blogs:
        blogs_json = jsonable_encoder([schemas.BlogRead(**blog.__dict__) for blog in blogs])
        cache.set_cache_blog_by_username(user.username, blogs_json)
    return blogs

def delete_blog(db : Session, id : int, user : models.User):
    delete_count = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user == user.id).delete(synchronize_session=False)
    db.commit()
    cache.del_cache_blog_by_username(user.username)
    cache.del_cache_blog_by_id(id)
    return delete_count

def update_blog(db : Session, id : int, user : models.User, update_data : schemas.BlogEdit):
    update_count = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user == user.id).update(update_data.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    cache.del_cache_blog_by_id(id)
    cache.del_cache_blog_by_username(user.username)
    return update_count