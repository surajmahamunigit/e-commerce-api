from slowapi import Limiter
from slowapi.util import get_remote_address
import os

# Limiter : imported by main.py and routes
limiter = Limiter(key_func=get_remote_address, enabled=os.getenv("TESTING") != "true")
