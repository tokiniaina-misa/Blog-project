import pytest
from blog.models import Category, Tag, Post, Comment, Profile
from blog.models_notification import Notification
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name='Tech')
    assert str(category) == 'Tech'

@pytest.mark.django_db
def test_tag_str():
    tag = Tag.objects.create(name='Python')
    assert str(tag) == 'Python'

@pytest.mark.django_db
def test_post_str():
    user = get_user_model().objects.create_user(username='author', email='author@example.com', password='pass')
    post = Post.objects.create(title='My Post', author=user)
    assert str(post) == 'My Post'

@pytest.mark.django_db
def test_comment_str():
    user = get_user_model().objects.create_user(username='commenter', email='commenter@example.com', password='pass')
    post = Post.objects.create(title='My Post', author=user)
    comment = Comment.objects.create(post=post, author=user, content='Nice!')
    assert str(comment) == f"Comment by {user.username} on {post.title}"


@pytest.mark.django_db
def test_profile_str():
    user = get_user_model().objects.create_user(username='profileuser', email='profile@example.com', password='pass')
    profile = Profile.objects.create(user=user)
    assert str(profile) == 'profileuser'

@pytest.mark.django_db
def test_notification_str():
    user = get_user_model().objects.create_user(username='notifuser', email='notif@example.com', password='pass')
    notification = Notification.objects.create(user=user, message='Hello!')
    assert str(notification) == f"Notification for {user.username}: Hello!"
