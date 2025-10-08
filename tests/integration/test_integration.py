import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post

@pytest.mark.django_db
class TestCoreIntegration:
    """Tests d'intégration essentiels"""
    
    def test_auth_workflow(self, client):
        """Test le workflow d'authentification complet"""
        # Création d'un utilisateur de test
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123'
        )
        
        # Test de connexion
        login_successful = client.login(username='testuser', password='SecurePass123')
        assert login_successful, "La connexion a échoué"
        
        # Vérification de l'accès à une page protégée
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 200, "L'accès à la page de profil a échoué"
    
    def test_blog_workflow(self, client):
        """Test le workflow de publication complet"""
        # Création utilisateur avec droits d'auteur
        user = User.objects.create_user(
            username='blogauthor',
            email='author@test.com',
            password='SecurePass123'
        )
        
        # Création du profil avec droits d'auteur
        from blog.models import Profile
        Profile.objects.create(user=user, is_author=True)
        
        # Connexion
        client.login(username='blogauthor', password='SecurePass123')
        
        # Création d'un post simple
        post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=user,
            status='published'
        )
        
        # Vérification de l'accès au post
        response = client.get(reverse('blog:post_detail', kwargs={'pk': post.pk}))
        assert response.status_code == 200, "Impossible d'accéder au post créé"
        
        # Vérification des données du post
        assert post.title == 'Test Post', "Le titre du post ne correspond pas"
        assert post.content == 'Test Content', "Le contenu du post ne correspond pas"
        assert post.author == user, "L'auteur du post ne correspond pas"
