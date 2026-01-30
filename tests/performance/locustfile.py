from locust import HttpUser, task, between

class GreenhouseUser(HttpUser):
    wait_time = between(1, 3)
    token = None
    
    def on_start(self):
        response = self.client.post("/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
    
    @task(3)
    def get_plants(self):
        if self.token:
            self.client.get("/api/plants", headers={
                "Authorization": f"Bearer {self.token}"
            })
    
    @task(2)
    def get_species(self):
        if self.token:
            self.client.get("/api/species", headers={
                "Authorization": f"Bearer {self.token}"
            })
    
    @task(1)
    def create_plant(self):
        if self.token:
            import time
            self.client.post("/api/plants", json={
                "name": f"Locust_{int(time.time())}",
                "speciesId": 1
            }, headers={
                "Authorization": f"Bearer {self.token}"
            })
    
    @task(1)
    def get_users(self):
        if self.token:
            self.client.get("/api/users", headers={
                "Authorization": f"Bearer {self.token}"
            })