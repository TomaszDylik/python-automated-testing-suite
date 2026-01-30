from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Species:
    id: int
    name: str
    drying_rate: float
    
    def validate(self):
        if not self.name:
            raise ValueError("Name is required")
        if self.drying_rate < 0:
            raise ValueError("Drying rate must be positive")
        return True

@dataclass
class Plant:
    id: int
    name: str
    species_id: int
    user_id: int
    current_water: float = 100.0
    is_dead: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Log:
    id: int
    message: str
    level: str
    plant_id: Optional[int] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()