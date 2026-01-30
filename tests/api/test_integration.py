import pytest
from config import API_URL
from helpers import unique_name

class TestIntegration:
    
    @pytest.mark.api
    def test_full_plant_lifecycle(self, auth_session):
        species_name = unique_name("IntegrationSpecies")
        species_response = auth_session.post(
            f"{API_URL}/api/species",
            json={"name": species_name, "dryingRate": 3.5}
        )
        assert species_response.status_code == 201
        species_id = species_response.json()["id"]
        
        plant_name = unique_name("IntegrationPlant")
        plant_response = auth_session.post(
            f"{API_URL}/api/plants",
            json={"name": plant_name, "speciesId": species_id}
        )
        assert plant_response.status_code == 201
        plant_id = plant_response.json()["id"]
        
        get_response = auth_session.get(f"{API_URL}/api/plants/{plant_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == plant_name
        
        updated_name = unique_name("UpdatedPlant")
        update_response = auth_session.put(
            f"{API_URL}/api/plants/{plant_id}",
            json={"name": updated_name, "currentWater": 75}
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == updated_name
        
        delete_response = auth_session.delete(f"{API_URL}/api/plants/{plant_id}")
        assert delete_response.status_code == 200
        
        verify_response = auth_session.get(f"{API_URL}/api/plants/{plant_id}")
        assert verify_response.status_code == 404
    
    @pytest.mark.api
    def test_user_registration_and_login_flow(self, api_session):
        username = unique_name("flowuser")
        password = "securepass123"
        
        register_response = api_session.post(
            f"{API_URL}/api/auth/register",
            json={"username": username, "password": password}
        )
        assert register_response.status_code == 201
        
        login_response = api_session.post(
            f"{API_URL}/api/auth/login",
            json={"username": username, "password": password}
        )
        assert login_response.status_code == 200
        assert "token" in login_response.json()