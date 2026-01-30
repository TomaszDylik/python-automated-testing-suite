import pytest
import sys
sys.path.insert(0, '..')

from app.services.user_service import UserService

class TestUserService:
    
    def setup_method(self):
        self.service = UserService()
    
    @pytest.mark.unit
    def test_register_user(self):
        user = self.service.register("testuser", "password123")
        
        assert user.username == "testuser"
        assert user.password_hash is not None
    
    @pytest.mark.unit
    def test_register_no_username(self):
        with pytest.raises(ValueError):
            self.service.register("", "password123")
    
    @pytest.mark.unit
    def test_register_no_password(self):
        with pytest.raises(ValueError):
            self.service.register("testuser", "")
    
    @pytest.mark.unit
    def test_register_short_password(self):
        with pytest.raises(ValueError):
            self.service.register("testuser", "123")
    
    @pytest.mark.unit
    def test_register_duplicate_username(self):
        self.service.register("testuser", "password123")
        with pytest.raises(ValueError):
            self.service.register("testuser", "otherpass")
    
    @pytest.mark.unit
    def test_login_success(self):
        self.service.register("testuser", "password123")
        user = self.service.login("testuser", "password123")
        
        assert user is not None
        assert user.username == "testuser"
    
    @pytest.mark.unit
    def test_login_wrong_password(self):
        self.service.register("testuser", "password123")
        user = self.service.login("testuser", "wrongpass")
        
        assert user is None
    
    @pytest.mark.unit
    def test_login_nonexistent_user(self):
        user = self.service.login("nouser", "password")
        assert user is None
    
    @pytest.mark.unit
    def test_login_empty_credentials(self):
        user = self.service.login("", "")
        assert user is None
    
    @pytest.mark.unit
    def test_get_user(self):
        created = self.service.register("testuser", "password123")
        user = self.service.get_user(created.id)
        
        assert user.username == "testuser"
    
    @pytest.mark.unit
    def test_get_user_not_found(self):
        user = self.service.get_user(999)
        assert user is None
    
    @pytest.mark.unit
    def test_get_all_users(self):
        self.service.register("user1", "password123")
        self.service.register("user2", "password123")
        
        users = self.service.get_all_users()
        assert len(users) == 2
    
    @pytest.mark.unit
    def test_update_user(self):
        created = self.service.register("testuser", "password123")
        updated = self.service.update_user(created.id, created.id, username="newname")
        
        assert updated.username == "newname"
    
    @pytest.mark.unit
    def test_update_user_access_denied(self):
        created = self.service.register("testuser", "password123")
        with pytest.raises(PermissionError):
            self.service.update_user(created.id, 999, username="hacked")
    
    @pytest.mark.unit
    def test_delete_user(self):
        created = self.service.register("testuser", "password123")
        result = self.service.delete_user(created.id, created.id)
        
        assert result is True
    
    @pytest.mark.unit
    def test_delete_user_access_denied(self):
        created = self.service.register("testuser", "password123")
        with pytest.raises(PermissionError):
            self.service.delete_user(created.id, 999)
    
    @pytest.mark.unit
    def test_search_users(self):
        self.service.register("admin", "password123")
        self.service.register("admin2", "password123")
        self.service.register("user", "password123")
        
        results = self.service.search_users("admin")
        assert len(results) == 2