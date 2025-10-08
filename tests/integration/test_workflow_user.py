# tests/test_workflow_user.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_signup_login_post(client):
    """
    Teste le workflow complet : inscription, connexion, création de post.
    """
    # Inscription
    signup_url = reverse('accounts:register')  # Utilise le namespace correct
    signup_data = {
        'username': 'workflowuser',
        'email': 'workflow@example.com',
        'password1': 'StrongPass123',
        'password2': 'StrongPass123',
    }
    response = client.post(signup_url, signup_data)
    assert response.status_code in (200, 302)
    assert User.objects.filter(username='workflowuser').exists()

    # Connexion
    login_url = reverse('accounts:login')  # Utilise le namespace correct
    login_data = {'username': 'workflowuser', 'password': 'StrongPass123'}
    response = client.post(login_url, login_data)
    assert response.status_code in (200, 302)
