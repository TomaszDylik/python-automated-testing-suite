import pytest
import time
from config import API_URL

class TestSpeciesAPI:
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_species_list(self, auth_session):
        response = auth_session.get(f"{API_URL}/api/species")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    @pytest.mark.api
    def test_get_species_unauthorized(self, api_session):
        response = api_session.get(f"{API_URL}/api/species")
        
        assert response.status_code == 401
    
    @pytest.mark.api
    def test_create_species(self, auth_session):
        species_name = f"TestSpecies_{int(time.time())}"
        species_data = {
            "name": species_name,
            "dryingRate": 5.5
        }
        
        response = auth_session.post(
            f"{API_URL}/api/species",
            json=species_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == species_name
    
    @pytest.mark.api
    def test_create_species_missing_name(self, auth_session):
        species_data = {
            "dryingRate": 5.5
        }
        
        response = auth_session.post(
            f"{API_URL}/api/species",
            json=species_data
        )
        
        assert response.status_code == 400
    
    @pytest.mark.api
    def test_create_species_missing_rate(self, auth_session):
        species_data = {
            "name": f"NoRate_{int(time.time())}"
        }
        
        response = auth_session.post(
            f"{API_URL}/api/species",
            json=species_data
        )
        
        assert response.status_code == 400
    
    @pytest.mark.api
    def test_create_species_invalid_rate(self, auth_session):
        species_data = {
            "name": f"InvalidRate_{int(time.time())}",
            "dryingRate": -5
        }
        
        response = auth_session.post(
            f"{API_URL}/api/species",
            json=species_data
        )
        
        assert response.status_code == 400
    
    @pytest.mark.api
    def test_get_single_species(self, auth_session):
        species_name = f"SingleSpec_{int(time.time())}"
        create_response = auth_session.post(
            f"{API_URL}/api/species",
            json={"name": species_name, "dryingRate": 3.0}
        )
        species_id = create_response.json()["id"]
        
        response = auth_session.get(f"{API_URL}/api/species/{species_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == species_id
    
    @pytest.mark.api
    def test_get_nonexistent_species(self, auth_session):
        response = auth_session.get(f"{API_URL}/api/species/99999")
        
        assert response.status_code == 404
    
    @pytest.mark.api
    def test_update_species(self, auth_session):
        species_name = f"UpdateSpec_{int(time.time())}"
        create_response = auth_session.post(
            f"{API_URL}/api/species",
            json={"name": species_name, "dryingRate": 4.0}
        )
        species_id = create_response.json()["id"]
        
        response = auth_session.put(
            f"{API_URL}/api/species/{species_id}",
            json={"name": f"Updated_{species_name}", "dryingRate": 6.0}
        )
        
        assert response.status_code == 200
    
    @pytest.mark.api
    def test_delete_species(self, auth_session):
        species_name = f"DeleteSpec_{int(time.time())}"
        create_response = auth_session.post(
            f"{API_URL}/api/species",
            json={"name": species_name, "dryingRate": 2.0}
        )
        species_id = create_response.json()["id"]
        
        response = auth_session.delete(f"{API_URL}/api/species/{species_id}")
        
        assert response.status_code == 200
    
    @pytest.mark.api
    def test_search_species(self, auth_session):
        response = auth_session.get(f"{API_URL}/api/species/search/Rose")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)