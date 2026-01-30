import pytest
import sys
sys.path.insert(0, '..')

from app.services.species_service import SpeciesService

class TestSpeciesService:
    
    def setup_method(self):
        self.service = SpeciesService()
    
    @pytest.mark.unit
    def test_create_species(self):
        species = self.service.create_species("Rose", 2.5)
        
        assert species.name == "Rose"
        assert species.drying_rate == 2.5
    
    @pytest.mark.unit
    def test_create_species_no_name(self):
        with pytest.raises(ValueError):
            self.service.create_species("", 2.5)
    
    @pytest.mark.unit
    def test_create_species_no_rate(self):
        with pytest.raises(ValueError):
            self.service.create_species("Rose", None)
    
    @pytest.mark.unit
    def test_create_species_negative_rate(self):
        with pytest.raises(ValueError):
            self.service.create_species("Rose", -1.0)
    
    @pytest.mark.unit
    def test_create_species_duplicate(self):
        self.service.create_species("Rose", 2.5)
        with pytest.raises(ValueError):
            self.service.create_species("rose", 3.0)
    
    @pytest.mark.unit
    def test_get_species(self):
        created = self.service.create_species("Rose", 2.5)
        species = self.service.get_species(created.id)
        
        assert species.name == "Rose"
    
    @pytest.mark.unit
    def test_get_species_not_found(self):
        species = self.service.get_species(999)
        assert species is None
    
    @pytest.mark.unit
    def test_get_all_species(self):
        self.service.create_species("Rose", 2.5)
        self.service.create_species("Tulip", 3.0)
        
        all_species = self.service.get_all_species()
        assert len(all_species) == 2
    
    @pytest.mark.unit
    def test_update_species(self):
        created = self.service.create_species("Rose", 2.5)
        updated = self.service.update_species(created.id, name="Red Rose")
        
        assert updated.name == "Red Rose"
    
    @pytest.mark.unit
    def test_update_species_rate(self):
        created = self.service.create_species("Rose", 2.5)
        updated = self.service.update_species(created.id, drying_rate=5.0)
        
        assert updated.drying_rate == 5.0
    
    @pytest.mark.unit
    def test_update_species_negative_rate(self):
        created = self.service.create_species("Rose", 2.5)
        with pytest.raises(ValueError):
            self.service.update_species(created.id, drying_rate=-1.0)
    
    @pytest.mark.unit
    def test_delete_species(self):
        created = self.service.create_species("Rose", 2.5)
        result = self.service.delete_species(created.id)
        
        assert result is True
    
    @pytest.mark.unit
    def test_delete_species_not_found(self):
        result = self.service.delete_species(999)
        assert result is False
    
    @pytest.mark.unit
    def test_search_species(self):
        self.service.create_species("Red Rose", 2.5)
        self.service.create_species("White Rose", 2.5)
        self.service.create_species("Tulip", 3.0)
        
        results = self.service.search_species("rose")
        assert len(results) == 2