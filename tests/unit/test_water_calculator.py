import pytest
import sys
sys.path.insert(0, '..')

from app.services.water_calculator import WaterCalculator

class TestWaterCalculator:
    
    def setup_method(self):
        self.calc = WaterCalculator(drying_rate=2.0)
    
    @pytest.mark.unit
    def test_calculate_water_loss(self):
        loss = self.calc.calculate_water_loss(5)
        assert loss == 10.0
    
    @pytest.mark.unit
    def test_calculate_water_loss_zero_hours(self):
        loss = self.calc.calculate_water_loss(0)
        assert loss == 0.0
    
    @pytest.mark.unit
    def test_calculate_water_loss_negative_hours(self):
        with pytest.raises(ValueError):
            self.calc.calculate_water_loss(-1)
    
    @pytest.mark.unit
    def test_calculate_remaining_water(self):
        remaining = self.calc.calculate_remaining_water(100, 10)
        assert remaining == 80.0
    
    @pytest.mark.unit
    def test_calculate_remaining_water_no_negative(self):
        remaining = self.calc.calculate_remaining_water(10, 100)
        assert remaining == 0
    
    @pytest.mark.unit
    def test_is_plant_dead_true(self):
        assert self.calc.is_plant_dead(0) is True
    
    @pytest.mark.unit
    def test_is_plant_dead_false(self):
        assert self.calc.is_plant_dead(50) is False
    
    @pytest.mark.unit
    def test_needs_watering_true(self):
        assert self.calc.needs_watering(20) is True
    
    @pytest.mark.unit
    def test_needs_watering_false(self):
        assert self.calc.needs_watering(50) is False
    
    @pytest.mark.unit
    def test_needs_watering_custom_threshold(self):
        assert self.calc.needs_watering(45, threshold=50) is True
    
    @pytest.mark.unit
    def test_water_plant(self):
        new_level = self.calc.water_plant(50, 30)
        assert new_level == 80
    
    @pytest.mark.unit
    def test_water_plant_max_100(self):
        new_level = self.calc.water_plant(80, 50)
        assert new_level == 100
    
    @pytest.mark.unit
    def test_water_plant_negative_amount(self):
        with pytest.raises(ValueError):
            self.calc.water_plant(50, -10)