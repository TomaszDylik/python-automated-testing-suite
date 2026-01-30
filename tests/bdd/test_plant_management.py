import pytest
from pytest_bdd import scenario, given, when, then, parsers
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.plant_service import PlantService
from app.services.user_service import UserService

# Scenarios
@pytest.mark.bdd
@scenario('features/plant_management.feature', 'Create a new plant')
def test_create_plant():
    pass

@pytest.mark.bdd
@scenario('features/plant_management.feature', 'View plant list')
def test_view_plant_list():
    pass

@pytest.mark.bdd
@scenario('features/plant_management.feature', 'Update plant water level')
def test_update_water_level():
    pass

@pytest.mark.bdd
@scenario('features/plant_management.feature', 'Delete a plant')
def test_delete_plant():
    pass

@pytest.mark.bdd
@scenario('features/plant_management.feature', 'Plant dies when water reaches zero')
def test_plant_dies():
    pass

@pytest.fixture
def plant_service():
    return PlantService()

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def context():
    return {}

@given(parsers.parse('I am logged in as "{username}"'))
def logged_in_user(user_service, context, username):
    try:
        user = user_service.register(username, "password123")
    except ValueError:
        user = user_service.login(username, "password123")
    context['user'] = user
    context['user_id'] = user.id

@given('I have plants in my collection')
def have_plants(plant_service, context):
    plant_service.create_plant("Plant 1", 1, context['user_id'])
    plant_service.create_plant("Plant 2", 1, context['user_id'])
    context['plant_service'] = plant_service

@given(parsers.parse('I have a plant named "{name}"'))
def have_plant(plant_service, context, name):
    plant = plant_service.create_plant(name, 1, context['user_id'])
    context['plant'] = plant
    context['plant_service'] = plant_service

@when(parsers.parse('I create a plant named "{name}" with species id {species_id:d}'))
def create_plant(plant_service, context, name, species_id):
    plant = plant_service.create_plant(name, species_id, context['user_id'])
    context['plant'] = plant
    context['plant_service'] = plant_service

@when('I request my plant list')
def request_plants(context):
    plants = context['plant_service'].get_user_plants(context['user_id'])
    context['plants'] = plants

@when(parsers.parse('I update the water level to {level:d}'))
def update_water(context, level):
    plant = context['plant_service'].update_plant(
        context['plant'].id, 
        context['user_id'], 
        water=level
    )
    context['plant'] = plant

@when('I delete the plant')
def delete_plant(context):
    result = context['plant_service'].delete_plant(
        context['plant'].id, 
        context['user_id']
    )
    context['deleted'] = result

@then('the plant should be created successfully')
def plant_created(context):
    assert context['plant'] is not None
    assert context['plant'].id > 0

@then(parsers.parse('the plant water level should be {level:d}'))
def check_water(context, level):
    assert context['plant'].current_water == level

@then('I should see all my plants')
def see_plants(context):
    assert len(context['plants']) >= 2

@then('the plant should not exist')
def plant_not_exist(context):
    assert context['deleted'] is True

@then('the plant should be marked as dead')
def plant_dead(context):
    assert context['plant'].is_dead is True