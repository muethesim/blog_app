from fastapi import FastAPI
from .routers import blogs, users, authentications
from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(authentications.router)