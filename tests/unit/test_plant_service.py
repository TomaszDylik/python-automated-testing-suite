import pytest
import sys
sys.path.insert(0, '..')

from app.services.plant_service import PlantService

class TestPlantService:
    
    def setup_method(self):
        self.service = PlantService()
    
    @pytest.mark.unit
    def test_create_plant(self):
        plant = self.service.create_plant("Rose", 1, 1)
        
        assert plant.name == "Rose"
        assert plant.species_id == 1
        assert plant.user_id == 1
        assert plant.current_water == 100.0
    
    @pytest.mark.unit
    def test_create_plant_no_name(self):
        with pytest.raises(ValueError):
            self.service.create_plant("", 1, 1)
    
    @pytest.mark.unit
    def test_create_plant_no_species(self):
        with pytest.raises(ValueError):
            self.service.create_plant("Rose", None, 1)
    
    @pytest.mark.unit
    def test_get_plant(self):
        created = self.service.create_plant("Rose", 1, 1)
        plant = self.service.get_plant(created.id, 1)
        
        assert plant is not None
        assert plant.name == "Rose"
    
    @pytest.mark.unit
    def test_get_plant_wrong_user(self):
        created = self.service.create_plant("Rose", 1, 1)
        plant = self.service.get_plant(created.id, 999)
        
        assert plant is None
    
    @pytest.mark.unit
    def test_get_plant_not_found(self):
        plant = self.service.get_plant(999, 1)
        assert plant is None
    
    @pytest.mark.unit
    def test_get_user_plants(self):
        self.service.create_plant("Rose", 1, 1)
        self.service.create_plant("Tulip", 1, 1)
        self.service.create_plant("Other", 1, 2)
        
        plants = self.service.get_user_plants(1)
        assert len(plants) == 2
    
    @pytest.mark.unit
    def test_update_plant(self):
        created = self.service.create_plant("Rose", 1, 1)
        updated = self.service.update_plant(created.id, 1, name="New Rose")
        
        assert updated.name == "New Rose"
    
    @pytest.mark.unit
    def test_update_plant_water(self):
        created = self.service.create_plant("Rose", 1, 1)
        updated = self.service.update_plant(created.id, 1, water=50)
        
        assert updated.current_water == 50
    
    @pytest.mark.unit
    def test_update_plant_dies_at_zero(self):
        created = self.service.create_plant("Rose", 1, 1)
        updated = self.service.update_plant(created.id, 1, water=0)
        
        assert updated.is_dead is True
    
    @pytest.mark.unit
    def test_delete_plant(self):
        created = self.service.create_plant("Rose", 1, 1)
        result = self.service.delete_plant(created.id, 1)
        
        assert result is True
        assert self.service.get_plant(created.id, 1) is None
    
    @pytest.mark.unit
    def test_delete_plant_not_found(self):
        result = self.service.delete_plant(999, 1)
        assert result is False
    
    @pytest.mark.unit
    def test_search_plants(self):
        self.service.create_plant("Red Rose", 1, 1)
        self.service.create_plant("White Rose", 1, 1)
        self.service.create_plant("Tulip", 1, 1)
        
        results = self.service.search_plants(1, "rose")
        assert len(results) == 2
    
    @pytest.mark.unit
    def test_get_dead_plants(self):
        plant = self.service.create_plant("Rose", 1, 1)
        self.service.update_plant(plant.id, 1, water=0)
        
        dead = self.service.get_dead_plants(1)
        assert len(dead) == 1