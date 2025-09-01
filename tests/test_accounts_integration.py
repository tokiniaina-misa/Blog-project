import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_register_view():
    client = Client()
    response = client.post(reverse('accounts:register'), {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'strongpassword',
        'password2': 'strongpassword',
    })
    assert response.status_code == 302  # Should redirect after registration

@pytest.mark.django_db
def test_login_view():
    User = get_user_model()
    User.objects.create_user(username='testuser', email='test@example.com', password='pass')
    client = Client()
    response = client.post(reverse('accounts:login'), {
        'username_or_email': 'testuser',
        'password': 'pass',
    })
    assert response.status_code == 302  # Should redirect after login
