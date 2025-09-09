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
        response = client.post(reverse('accounts:register'), signup_data, follow=True)
        assert response.status_code == 200  # Succès après redirection
        
        # Vérifier que l'utilisateur est créé
        assert User.objects.filter(username='integrationuser').exists()
        
        # Connexion
        login_data = {
            'username': 'integrationuser',
            'password': 'SecurePass123'
        }
        response = client.post(reverse('accounts:login'), login_data, follow=True)
        assert response.status_code == 200  # Succès après redirection
        # Vérifier que l'utilisateur est connecté
        assert '_auth_user_id' in client.session
    
    def test_blog_workflow(self, client):
        """Test le workflow de publication complet"""
        # Création utilisateur et connexion
        user = User.objects.create_user(
            username='blogger',
            password='SecurePass123'
        )
        success = client.login(username='blogger', password='SecurePass123')
        assert success, "Login failed"
        
        # Création article
        post_data = {
            'title': 'Integration Test',
            'content': 'Test Content',
            'is_draft': False,
            'author': user.id  # Ajout de l'auteur explicitement
        }
        
        # S'assurer que l'URL existe
        create_url = reverse('blog:post_create')
        response = client.post(create_url, post_data, follow=True)
        
        if response.status_code != 302 and response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content}")
            
        assert response.status_code in [200, 302], f"Unexpected status code: {response.status_code}"
        
        # Vérification article créé avec plus de détails en cas d'échec
        try:
            post = Post.objects.get(title='Integration Test')
            assert post.author == user
            assert post.content == 'Test Content'
            
            # Test accès à l'article
            detail_url = reverse('blog:post_detail', kwargs={'pk': post.pk})
            response = client.get(detail_url)
            assert response.status_code == 200
            
        except Post.DoesNotExist:
            # Informations de débogage en cas d'échec
            existing_posts = Post.objects.all()
            print(f"Posts existants: {[p.title for p in existing_posts]}")
            print(f"Données de la requête: {post_data}")
            raise
