import pytest
from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.contrib.auth.models import User
from blog.models import Post
from django.test import Client

@pytest.mark.django_db
class TestPerformance:
    """Tests de performance essentiels pour la pipeline DevOps"""
    
    def test_blog_list_query_performance(self, client):
        """Test la performance des requêtes de la liste des articles"""
        # Création des données de test
        user = User.objects.create_user(username='perftest', password='testpass123')
        for i in range(10):
            Post.objects.create(
                title=f'Performance Test {i}',
                content='Content',
                author=user
            )
            
        # Test du nombre de requêtes
        with CaptureQueriesContext(connection) as captured:
            response = client.get(reverse('blog:post_list'))
            assert response.status_code == 200
            assert len(captured.captured_queries) <= 5  # Max 5 requêtes

    def test_api_response_time(self, client):
        """Test le temps de réponse de l'API"""
        import time
        
        # Création d'un article
        user = User.objects.create_user(username='speedtest', password='testpass123')
        post = Post.objects.create(
            title='Speed Test',
            content='Content',
            author=user
        )
        
        # Test du temps de réponse
        start_time = time.time()
        response = client.get(reverse('blog:post_detail', kwargs={'pk': post.pk}))
        end_time = time.time()
        
        assert response.status_code == 200
        assert end_time - start_time < 0.3  # Maximum 300ms
