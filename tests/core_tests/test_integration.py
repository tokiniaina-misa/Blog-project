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
        user = User.objects.get(username='integrationuser')
        assert user.is_active
        
        # Connexion
        success = client.login(username='integrationuser', password='SecurePass123')
        assert success, "Login failed"
        
        # Vérifier que l'utilisateur est connecté
        response = client.get(reverse('accounts:profile'))  # Tente d'accéder à une page protégée
        assert response.status_code == 200, "L'utilisateur n'est pas correctement connecté"
    
    def test_blog_workflow(self, client):
        """Test le workflow de publication complet"""
        # Création utilisateur avec les permissions nécessaires
        user = User.objects.create_user(
            username='blogger',
            password='SecurePass123',
            email='blogger@test.com'
        )
        # Assurer que l'utilisateur a les permissions d'auteur
        from blog.models import Profile
        Profile.objects.create(user=user, is_author=True)
        
        # Connexion
        success = client.login(username='blogger', password='SecurePass123')
        assert success, "Login failed"
        
        # Création article avec les champs minimaux requis
        post_data = {
            'title': 'Integration Test',
            'content': 'Test Content',
            'status': 'published'  # ou le champ approprié selon votre modèle
        }
        
        # Debug: Afficher les URLs disponibles
        from django.urls import get_resolver
        urls = get_resolver().reverse_dict.keys()
        print(f"URLs disponibles : {[url for url in urls if isinstance(url, str)]}")
        
        # Création de l'article
        create_url = reverse('blog:post_create')
        response = client.post(create_url, post_data, follow=True)
        
        # Debug en cas d'échec
        if response.status_code not in [200, 302]:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.content.decode()}")
            
        assert response.status_code in [200, 302], f"Unexpected status code: {response.status_code}"
        
        # Vérification de la création de l'article avec plus de détails
        try:
            post = Post.objects.get(title='Integration Test')
            assert post.author == user, f"Author mismatch: expected {user}, got {post.author}"
            assert post.content == 'Test Content', f"Content mismatch: expected 'Test Content', got {post.content}"
            
            # Test d'accès à l'article
            detail_url = reverse('blog:post_detail', kwargs={'pk': post.pk})
            response = client.get(detail_url)
            assert response.status_code == 200, f"Cannot access post details, status: {response.status_code}"
            
        except Post.DoesNotExist:
            # Information détaillée en cas d'échec
            print(f"Test user: {user.username} (ID: {user.id})")
            print(f"Test user permissions: {user.get_all_permissions()}")
            print(f"Form data sent: {post_data}")
            print(f"Response content: {response.content.decode()}")
            existing_posts = Post.objects.all().values('id', 'title', 'author_id')
            print(f"Existing posts: {list(existing_posts)}")
            raise
