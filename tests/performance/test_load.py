import pytest
import time
import statistics
from config import API_URL

class TestPerformance:
    
    @pytest.mark.performance
    def test_login_response_time(self, api_session):
        times = []
        
        for _ in range(100):
            start = time.time()
            response = api_session.post(
                f"{API_URL}/api/auth/login",
                json={"username": "user1", "password": "user123"}
            )
            end = time.time()
            times.append(end - start)
        
        avg_time = statistics.mean(times)
        max_time = max(times)
        
        assert avg_time < 0.5
        assert max_time < 2.0
        
        print(f"\nLogin Performance:")
        print(f"  Average: {avg_time:.3f}s")
        print(f"  Max: {max_time:.3f}s")
        print(f"  Min: {min(times):.3f}s")
    
    @pytest.mark.performance
    def test_get_plants_response_time(self, auth_session):
        times = []
        
        for _ in range(50):
            start = time.time()
            response = auth_session.get(f"{API_URL}/api/plants")
            end = time.time()
            times.append(end - start)
        
        avg_time = statistics.mean(times)
        
        assert avg_time < 0.3
        
        print(f"\nGet Plants Performance:")
        print(f"  Average: {avg_time:.3f}s")
        print(f"  Requests: 50")
    
    @pytest.mark.performance
    def test_create_plant_under_load(self, auth_session):
        times = []
        created_ids = []
        
        for i in range(20):
            start = time.time()
            response = auth_session.post(
                f"{API_URL}/api/plants",
                json={"name": f"LoadTest_{i}", "speciesId": 1}
            )
            end = time.time()
            times.append(end - start)
            
            if response.status_code == 201:
                created_ids.append(response.json()["id"])
        
        avg_time = statistics.mean(times)
        
        for plant_id in created_ids:
            auth_session.delete(f"{API_URL}/api/plants/{plant_id}")
        
        assert avg_time < 0.5
        
        print(f"\nCreate Plant Performance:")
        print(f"  Average: {avg_time:.3f}s")
        print(f"  Created: {len(created_ids)}")
    
    @pytest.mark.performance
    def test_concurrent_species_requests(self, auth_session):
        times = []
        
        for _ in range(100):
            start = time.time()
            response = auth_session.get(f"{API_URL}/api/species")
            end = time.time()
            times.append(end - start)
            
            assert response.status_code == 200
        
        avg_time = statistics.mean(times)
        p95 = sorted(times)[94]
        
        assert avg_time < 0.2
        assert p95 < 0.5
        
        print(f"\nSpecies List Performance:")
        print(f"  Average: {avg_time:.3f}s")
        print(f"  P95: {p95:.3f}s")