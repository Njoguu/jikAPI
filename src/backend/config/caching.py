import os
from flask_caching import Cache


redis_config = {
    # "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "RedisCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_REDIS_URL": os.getenv("REDIS_URL")
}

cache = Cache(config=redis_config)

def init_cache(app):
    # Initialize the cache
    cache.init_app(app)
