import pytest
import requests
from config import API_URL, TEST_USER

@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session

@pytest.fixture(scope="session")
def auth_token(api_session):
    response = api_session.post(
        f"{API_URL}/api/auth/login",
        json=TEST_USER
    )
    if response.status_code == 200:
        return response.json().get("token")
    return None

@pytest.fixture(scope="session")
def auth_session(api_session, auth_token):
    if auth_token:
        api_session.headers.update({"Authorization": f"Bearer {auth_token}"})
    return api_session