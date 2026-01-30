class WaterCalculator:
    
    def __init__(self, drying_rate: float):
        self.drying_rate = drying_rate
    
    def calculate_water_loss(self, hours: int) -> float:
        if hours < 0:
            raise ValueError("Hours cannot be negative")
        return self.drying_rate * hours
    
    def calculate_remaining_water(self, current: float, hours: int) -> float:
        loss = self.calculate_water_loss(hours)
        remaining = current - loss
        return max(0, remaining)
    
    def is_plant_dead(self, current_water: float) -> bool:
        return current_water <= 0
    
    def needs_watering(self, current_water: float, threshold: float = 30.0) -> bool:
        return current_water < threshold
    
    def water_plant(self, current_water: float, amount: float) -> float:
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        new_level = current_water + amount
        return min(100, new_level)