from typing import List, Optional
from app.models import Plant, Log

class PlantService:
    
    def __init__(self, db_client=None):
        self.db = db_client
        self.plants = []
        self.logs = []
    
    def create_plant(self, name: str, species_id: int, user_id: int) -> Plant:
        if not name:
            raise ValueError("Name is required")
        if not species_id:
            raise ValueError("Species ID is required")
        
        plant_id = len(self.plants) + 1
        plant = Plant(
            id=plant_id,
            name=name,
            species_id=species_id,
            user_id=user_id
        )
        self.plants.append(plant)
        self._add_log(f"Plant {name} created", "INFO", plant_id)
        return plant
    
    def get_plant(self, plant_id: int, user_id: int) -> Optional[Plant]:
        for plant in self.plants:
            if plant.id == plant_id and plant.user_id == user_id:
                return plant
        return None
    
    def get_user_plants(self, user_id: int) -> List[Plant]:
        return [p for p in self.plants if p.user_id == user_id and not p.is_dead]
    
    def get_dead_plants(self, user_id: int) -> List[Plant]:
        return [p for p in self.plants if p.user_id == user_id and p.is_dead]
    
    def update_plant(self, plant_id: int, user_id: int, name: str = None, water: float = None) -> Optional[Plant]:
        plant = self.get_plant(plant_id, user_id)
        if not plant:
            return None
        
        if name:
            plant.name = name
        if water is not None:
            plant.current_water = max(0, min(100, water))
            if plant.current_water <= 0:
                plant.is_dead = True
                self._add_log(f"Plant {plant.name} died", "WARNING", plant_id)
        
        return plant
    
    def delete_plant(self, plant_id: int, user_id: int) -> bool:
        plant = self.get_plant(plant_id, user_id)
        if not plant:
            return False
        
        self.plants.remove(plant)
        self._add_log(f"Plant {plant.name} deleted", "WARNING", None)
        return True
    
    def search_plants(self, user_id: int, pattern: str) -> List[Plant]:
        return [p for p in self.plants 
                if p.user_id == user_id and pattern.lower() in p.name.lower()]
    
    def _add_log(self, message: str, level: str, plant_id: int):
        log = Log(
            id=len(self.logs) + 1,
            message=message,
            level=level,
            plant_id=plant_id
        )
        self.logs.append(log)