import pytest
from blog.models import Post
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_post_str():
    user = get_user_model().objects.create_user(username='author', password='pass')
    post = Post.objects.create(title='Test', author=user)
    assert str(post) == 'Test'
