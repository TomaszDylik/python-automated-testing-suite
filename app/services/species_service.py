from typing import List, Optional
from app.models import Species

class SpeciesService:
    
    def __init__(self, db_client=None):
        self.db = db_client
        self.species_list = []
    
    def create_species(self, name: str, drying_rate: float) -> Species:
        if not name:
            raise ValueError("Name is required")
        if drying_rate is None:
            raise ValueError("Drying rate is required")
        if drying_rate < 0:
            raise ValueError("Drying rate must be positive")
        
        for s in self.species_list:
            if s.name.lower() == name.lower():
                raise ValueError("Species already exists")
        
        species = Species(
            id=len(self.species_list) + 1,
            name=name,
            drying_rate=drying_rate
        )
        self.species_list.append(species)
        return species
    
    def get_species(self, species_id: int) -> Optional[Species]:
        for species in self.species_list:
            if species.id == species_id:
                return species
        return None
    
    def get_all_species(self) -> List[Species]:
        return self.species_list.copy()
    
    def update_species(self, species_id: int, name: str = None, drying_rate: float = None) -> Optional[Species]:
        species = self.get_species(species_id)
        if not species:
            return None
        
        if name:
            species.name = name
        if drying_rate is not None:
            if drying_rate < 0:
                raise ValueError("Drying rate must be positive")
            species.drying_rate = drying_rate
        
        return species
    
    def delete_species(self, species_id: int) -> bool:
        species = self.get_species(species_id)
        if not species:
            return False
        
        self.species_list.remove(species)
        return True
    
    def search_species(self, pattern: str) -> List[Species]:
        return [s for s in self.species_list 
                if pattern.lower() in s.name.lower()]