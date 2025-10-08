import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_invalid_post_access(client):
    user = User.objects.create_user(username='author', password='pass')
    client.login(username='author', password='pass')
    url = reverse('blog:post_detail', kwargs={'pk': 9999})
    response = client.get(url)
    assert response.status_code == 404
