import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
API_URL = os.getenv("API_URL", "http://localhost:3001")

TEST_USER = {
    "username": "testuser",
    "password": "test123"
}

ADMIN_USER = {
    "username": "admin",
    "password": "admin123"
}

TIMEOUT = 10