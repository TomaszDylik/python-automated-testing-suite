import hashlib
from typing import Optional
from app.models import User

class UserService:
    
    def __init__(self, db_client=None):
        self.db = db_client
        self.users = []
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username: str, password: str) -> User:
        if not username:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")
        if len(password) < 6:
            raise ValueError("Password too short")
        
        for u in self.users:
            if u.username == username:
                raise ValueError("Username already exists")
        
        user = User(
            id=len(self.users) + 1,
            username=username,
            password_hash=self._hash_password(password)
        )
        self.users.append(user)
        return user
    
    def login(self, username: str, password: str) -> Optional[User]:
        if not username or not password:
            return None
        
        password_hash = self._hash_password(password)
        for user in self.users:
            if user.username == username and user.password_hash == password_hash:
                return user
        return None
    
    def get_user(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_all_users(self):
        return [{"id": u.id, "username": u.username} for u in self.users]
    
    def update_user(self, user_id: int, requesting_user_id: int, username: str = None, password: str = None) -> Optional[User]:
        if user_id != requesting_user_id:
            raise PermissionError("Access denied")
        
        user = self.get_user(user_id)
        if not user:
            return None
        
        if username:
            user.username = username
        if password:
            user.password_hash = self._hash_password(password)
        
        return user
    
    def delete_user(self, user_id: int, requesting_user_id: int) -> bool:
        if user_id != requesting_user_id:
            raise PermissionError("Access denied")
        
        user = self.get_user(user_id)
        if not user:
            return False
        
        self.users.remove(user)
        return True
    
    def search_users(self, pattern: str):
        return [{"id": u.id, "username": u.username} 
                for u in self.users if pattern.lower() in u.username.lower()]