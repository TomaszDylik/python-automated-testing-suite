import pytest
import requests
from config import API_URL

class TestAuthAPI:
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_success(self, api_session):
        response = api_session.post(
            f"{API_URL}/api/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user" in data
    
    @pytest.mark.api
    def test_login_invalid_password(self, api_session):
        response = api_session.post(
            f"{API_URL}/api/auth/login",
            json={"username": "admin", "password": "wrongpass"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.api
    def test_login_nonexistent_user(self, api_session):
        response = api_session.post(
            f"{API_URL}/api/auth/login",
            json={"username": "nouser", "password": "pass123"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.api
    def test_login_empty_credentials(self, api_session):
        response = api_session.post(
            f"{API_URL}/api/auth/login",
            json={"username": "", "password": ""}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.api
    def test_register_new_user(self, api_session):
        import time
        unique_user = f"testuser_{int(time.time())}"
        
        response = api_session.post(
            f"{API_URL}/api/auth/register",
            json={"username": unique_user, "password": "password123"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "token" in data
    
    @pytest.mark.api
    def test_register_duplicate_user(self, api_session):
        response = api_session.post(
            f"{API_URL}/api/auth/register",
            json={"username": "admin", "password": "password123"}
        )
        
        assert response.status_code == 400