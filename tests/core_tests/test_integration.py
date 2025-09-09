import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

@pytest.mark.django_db
class TestCoreIntegration:
    """Tests d'intégration essentiels"""
    
    def test_auth_workflow(self, client):
        """Test le workflow d'authentification complet"""
        # Création compte
        signup_data = {
            'username': 'integrationuser',
            'email': 'integration@test.com',
            'password1': 'SecurePass123',
            'password2': 'SecurePass123'
        }
        response = client.post(reverse('accounts:register'), signup_data)
        assert response.status_code == 302  # Redirection après création
        
        # Connexion
        login_data = {
            'username': 'integrationuser',
            'password': 'SecurePass123'
        }
        response = client.post(reverse('accounts:login'), login_data)
        assert response.status_code == 302  # Redirection après connexion
    
    def test_blog_workflow(self, client):
        """Test le workflow de publication complet"""
        # Création utilisateur et connexion
        user = User.objects.create_user(
            username='blogger',
            password='SecurePass123'
        )
        client.login(username='blogger', password='SecurePass123')
        
        # Création article
        post_data = {
            'title': 'Integration Test',
            'content': 'Test Content',
            'is_draft': False
        }
        response = client.post(reverse('blog:post_create'), post_data)
        assert response.status_code == 302
        
        # Vérification article créé
        post = Post.objects.get(title='Integration Test')
        assert post.author == user
        
        # Test accès à l'article
        response = client.get(
            reverse('blog:post_detail', kwargs={'pk': post.pk})
        )
        assert response.status_code == 200
