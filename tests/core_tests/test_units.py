import pytest
from django.contrib.auth.models import User
from blog.models import Post
from accounts.forms.register_form import RegisterForm

@pytest.mark.django_db
class TestCoreUnits:
    """Tests unitaires essentiels pour les fonctionnalités core"""
    
    def test_user_creation(self):
        """Test la création d'utilisateur - Critique pour l'authentification"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.is_active
    
    def test_post_creation(self):
        """Test la création d'article - Fonctionnalité métier principale"""
        author = User.objects.create_user(username='author', password='pass123')
        post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=author,
            is_draft=False
        )
        assert post.title == 'Test Post'
        assert post.author == author
        assert not post.is_draft
    
    def test_register_form_validation(self):
        """Test la validation du formulaire d'inscription - Sécurité critique"""
        form_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "SecurePass123",
            "password2": "SecurePass123"
        }
        form = RegisterForm(data=form_data)
        assert form.is_valid()
