import pytest
from unittest.mock import Mock, patch
import sys
sys.path.insert(0, '..')

from app.services.external_api import ExternalWeatherAPI, GreenhouseController

class TestGreenhouseController:
    
    def setup_method(self):
        self.mock_api = Mock(spec=ExternalWeatherAPI)
        self.controller = GreenhouseController(self.mock_api)
    
    @pytest.mark.unit
    def test_should_water_hot_weather(self):
        self.mock_api.get_temperature.return_value = 35.0
        self.mock_api.get_humidity.return_value = 50.0
        
        result = self.controller.should_water_plants("Warsaw", 55)
        assert result is True
    
    @pytest.mark.unit
    def test_should_not_water_cool_weather(self):
        self.mock_api.get_temperature.return_value = 20.0
        self.mock_api.get_humidity.return_value = 60.0
        
        result = self.controller.should_water_plants("Warsaw", 50)
        assert result is False
    
    @pytest.mark.unit
    def test_should_water_low_humidity(self):
        self.mock_api.get_temperature.return_value = 25.0
        self.mock_api.get_humidity.return_value = 30.0
        
        result = self.controller.should_water_plants("Warsaw", 45)
        assert result is True
    
    @pytest.mark.unit
    def test_should_water_api_failure(self):
        self.mock_api.get_temperature.return_value = None
        self.mock_api.get_humidity.return_value = None
        
        result = self.controller.should_water_plants("Warsaw", 40)
        assert result is True
    
    @pytest.mark.unit
    def test_water_adjustment_hot(self):
        self.mock_api.get_temperature.return_value = 38.0
        
        adjustment = self.controller.calculate_water_adjustment("Warsaw")
        assert adjustment == 1.5
    
    @pytest.mark.unit
    def test_water_adjustment_warm(self):
        self.mock_api.get_temperature.return_value = 28.0
        
        adjustment = self.controller.calculate_water_adjustment("Warsaw")
        assert adjustment == 1.2
    
    @pytest.mark.unit
    def test_water_adjustment_cold(self):
        self.mock_api.get_temperature.return_value = 5.0
        
        adjustment = self.controller.calculate_water_adjustment("Warsaw")
        assert adjustment == 0.8
    
    @pytest.mark.unit
    def test_water_adjustment_normal(self):
        self.mock_api.get_temperature.return_value = 20.0
        
        adjustment = self.controller.calculate_water_adjustment("Warsaw")
        assert adjustment == 1.0
    
    @pytest.mark.unit
    def test_water_adjustment_api_failure(self):
        self.mock_api.get_temperature.return_value = None
        
        adjustment = self.controller.calculate_water_adjustment("Warsaw")
        assert adjustment == 1.0