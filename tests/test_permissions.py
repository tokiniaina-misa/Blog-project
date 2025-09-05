# tests/test_permissions.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_access_protected_view(client):
    """
    Vérifie qu'un utilisateur non authentifié est redirigé depuis une vue protégée.
    """
    url = reverse('accounts:profile')  # Utilise le namespace correct
    response = client.get(url)
    assert response.status_code == 302  # Redirection vers la page de login

@pytest.mark.django_db
def test_access_protected_view_authenticated(client):
    """
    Vérifie qu'un utilisateur authentifié accède à la vue protégée.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    url = reverse('accounts:profile')  # Utilise le namespace correct
    response = client.get(url)
    assert response.status_code == 200
