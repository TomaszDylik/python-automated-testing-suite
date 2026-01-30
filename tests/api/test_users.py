import pytest
import time
from config import API_URL

class TestUsersAPI:
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_users_list(self, auth_session):
        response = auth_session.get(f"{API_URL}/api/users")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    @pytest.mark.api
    def test_get_users_unauthorized(self, api_session):
        response = api_session.get(f"{API_URL}/api/users")
        
        assert response.status_code == 401
    
    @pytest.mark.api
    def test_get_user_by_id(self, auth_session):
        users = auth_session.get(f"{API_URL}/api/users").json()
        if len(users) > 0:
            user_id = users[0]["id"]
            
            response = auth_session.get(f"{API_URL}/api/users/{user_id}")
            
            assert response.status_code == 200
            assert response.json()["id"] == user_id
    
    @pytest.mark.api
    def test_get_nonexistent_user(self, auth_session):
        response = auth_session.get(f"{API_URL}/api/users/99999")
        
        assert response.status_code == 404
    
    @pytest.mark.api
    def test_search_users(self, auth_session):
        response = auth_session.get(f"{API_URL}/api/users?search=admin")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    @pytest.mark.api
    def test_update_own_user(self, api_session):
        unique_user = f"updatetest_{int(time.time())}"
        register_response = api_session.post(
            f"{API_URL}/api/auth/register",
            json={"username": unique_user, "password": "password123"}
        )
        
        token = register_response.json()["token"]
        user_id = register_response.json()["user"]["id"]
        
        api_session.headers.update({"Authorization": f"Bearer {token}"})
        
        response = api_session.put(
            f"{API_URL}/api/users/{user_id}",
            json={"username": f"updated_{unique_user}"}
        )
        
        assert response.status_code == 200
    
    @pytest.mark.api
    def test_update_other_user_forbidden(self, auth_session):
        response = auth_session.put(
            f"{API_URL}/api/users/99999",
            json={"username": "hacked"}
        )
        
        assert response.status_code == 403