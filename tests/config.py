import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
API_URL = os.getenv("API_URL", "http://localhost:3001")

TEST_USER = {
    "username": "user1",
    "password": "user123"
}

ADMIN_USER = {
    "username": "user1",
    "password": "user123"
}

TIMEOUT = 10