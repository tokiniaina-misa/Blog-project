import pytest
from django.test import Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def test_password():
    return 'SecurePass123'

@pytest.fixture
def test_user(db, django_user_model, test_password):
    user = django_user_model.objects.create_user(
        username='testuser',
        password=test_password,
        email='test@example.com'
    )
    return user

@pytest.fixture
def authenticated_client(client, test_user, test_password):
    client.login(username=test_user.username, password=test_password)
    return client
