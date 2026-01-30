import pytest
import sys
sys.path.insert(0, '..')

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