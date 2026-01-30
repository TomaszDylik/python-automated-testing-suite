import requests
from typing import Optional

class ExternalWeatherAPI:
    
    def __init__(self, api_url: str = "https://api.weather.example.com"):
        self.api_url = api_url
    
    def get_temperature(self, location: str) -> Optional[float]:
        try:
            response = requests.get(f"{self.api_url}/temp/{location}")
            if response.status_code == 200:
                return response.json().get("temperature")
        except:
            pass
        return None
    
    def get_humidity(self, location: str) -> Optional[float]:
        try:
            response = requests.get(f"{self.api_url}/humidity/{location}")
            if response.status_code == 200:
                return response.json().get("humidity")
        except:
            pass
        return None

class GreenhouseController:
    
    def __init__(self, weather_api: ExternalWeatherAPI):
        self.weather_api = weather_api
    
    def should_water_plants(self, location: str, current_water: float) -> bool:
        temp = self.weather_api.get_temperature(location)
        humidity = self.weather_api.get_humidity(location)
        
        if temp is None or humidity is None:
            return current_water < 50
        
        if temp > 30:
            return current_water < 60
        if humidity < 40:
            return current_water < 50
        
        return current_water < 30
    
    def calculate_water_adjustment(self, location: str) -> float:
        temp = self.weather_api.get_temperature(location)
        if temp is None:
            return 1.0
        
        if temp > 35:
            return 1.5
        elif temp > 25:
            return 1.2
        elif temp < 10:
            return 0.8
        
        return 1.0