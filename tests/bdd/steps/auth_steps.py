import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
sys.path.insert(0, '../..')

from app.services.user_service import UserService

scenarios('../features/user_auth.feature')

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def context():
    return {}

@given(parsers.parse('a user "{username}" with password "{password}" exists'))
def user_exists(user_service, context, username, password):
    try:
        user_service.register(username, password)
    except ValueError:
        pass
    context['user_service'] = user_service

@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login(context, username, password):
    user_service = context.get('user_service', UserService())
    context['user_service'] = user_service
    try:
        user = user_service.login(username, password)
        context['result'] = user
        context['error'] = None
    except Exception as e:
        context['result'] = None
        context['error'] = str(e)

@when(parsers.parse('I register with username "{username}" and password "{password}"'))
def register(context, username, password):
    user_service = context.get('user_service', UserService())
    context['user_service'] = user_service
    try:
        user = user_service.register(username, password)
        context['result'] = user
        context['error'] = None
    except ValueError as e:
        context['result'] = None
        context['error'] = str(e)

@then('I should receive a valid token')
def valid_token(context):
    assert context['result'] is not None

@then('I should get an authentication error')
def auth_error(context):
    assert context['result'] is None

@then('the user should be created')
def user_created(context):
    assert context['result'] is not None
    assert context['result'].id > 0

@then('I should get a registration error')
def reg_error(context):
    assert context['error'] is not None