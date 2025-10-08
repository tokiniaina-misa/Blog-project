import pytest
from django.contrib.auth.models import User
from blog.models import Post, Comment, Profile
from blog.models_notification import Notification

@pytest.mark.django_db
def test_notification_on_comment(client):
    user = User.objects.create_user(username='author', password='pass')
    profile = Profile.objects.create(user=user, notification_enabled=True)
    client.login(username='author', password='pass')
    post = Post.objects.create(title='Notif Post', author=user)
    comment = Comment.objects.create(post=post, author=user, content='Test')
    Notification.objects.create(user=user, message='New comment')
    assert Notification.objects.filter(user=user).exists()
