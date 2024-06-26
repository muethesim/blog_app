from redis import Redis

redis = Redis(host="127.0.0.1", port="6379", charset="utf-8", decode_responses=True)

# redis.hset("test", mapping={"abc":123, "mno":456})

print(type(redis.hgetall("test")))