import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_admin_dashboard_access(client):
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
    client.login(username='admin', password='adminpass')
    url = reverse('blog:admin_dashboard')
    response = client.get(url)
    assert response.status_code == 200
