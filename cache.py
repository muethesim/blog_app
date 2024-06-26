import redis as redis_cls
from typing import Any
from dotenv import load_dotenv
import os
import json

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
expiry_time = os.getenv("REDIS_EXPIRY_TIME")

redis = redis_cls.Redis(host=redis_host, port=redis_port, charset="utf-8", decode_responses=True)

def get_cache_blog(key:str):
    blog_data = redis.get(key)
    return json.loads(blog_data) if blog_data else None

def set_cache_blog(key:str, value:Any):
    return redis.set(key, json.dumps(value), ex=expiry_time)

def del_cache_blog(key:str):
    return redis.delete(key)



def set_cache_blog_by_id(id:int, value:Any):
    return set_cache_blog(f"blog_id:{id}", value)

def set_cache_blog_by_username(username:str, value : Any):
    return set_cache_blog(f"blog_user:{username}", value)

def get_cache_blog_by_id(id:int):
    return get_cache_blog(f"blog_id:{id}")

def get_cache_blog_by_username(username:str):
    return get_cache_blog(f"blog_user:{username}")

def del_cache_blog_by_id(id:int):
    return del_cache_blog(f"blog_id:{id}")

def del_cache_blog_by_username(username:str):
    return del_cache_blog(f"blog_user:{username}")

