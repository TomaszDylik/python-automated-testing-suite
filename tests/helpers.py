import random
import string
import time

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_email():
    return f"{random_string(8)}@test.com"

def unique_name(prefix="test"):
    return f"{prefix}_{int(time.time())}_{random_string(4)}"

def wait_seconds(seconds):
    time.sleep(seconds)