import pytest
from django.contrib.auth.models import User
from blog.models import Post
from django.urls import reverse

@pytest.mark.django_db
def test_post_list_pagination(client):
    user = User.objects.create_user(username='author', password='pass')
    client.login(username='author', password='pass')
    for i in range(15):
        Post.objects.create(title=f'Post {i}', author=user)
    url = reverse('blog:post_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context
