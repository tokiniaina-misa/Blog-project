import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from blog.models import Post

@pytest.mark.django_db
def test_post_create_view():
    User = get_user_model()
    user = User.objects.create_user(username='author', email='author@example.com', password='pass')
    from blog.models import Profile
    Profile.objects.create(user=user, is_author=True)
    client = Client()
    client.force_login(user)
    response = client.post(reverse('blog:post_create'), {
        'title': 'Test Post',
        'content': 'Some content',
        'categories': ['RPG'],
        'tags': ['review'],
    })
    assert response.status_code == 302
    assert Post.objects.filter(title='Test Post').exists()

@pytest.mark.django_db
def test_post_list_view():
    client = Client()
    response = client.get(reverse('blog:post_list'))
    assert response.status_code == 200
