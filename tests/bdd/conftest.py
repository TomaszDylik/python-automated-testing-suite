import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.plant_service import PlantService
from app.services.user_service import UserService
from app.services.species_service import SpeciesService

@pytest.fixture
def plant_service():
    return PlantService()

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def species_service():
    return SpeciesService()