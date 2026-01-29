import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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

@pytest.fixture(scope="function")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    driver.set_window_size(1920, 1080)
    
    yield driver
    
    driver.quit()