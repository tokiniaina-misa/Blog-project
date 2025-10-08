# À déplacer ici : tests sur la base de données
import pytest
from django.db import connection
from django.contrib.auth.models import User
from blog.models import Post, Comment
from django.test.utils import CaptureQueriesContext

@pytest.mark.django_db
class TestDatabaseIntegration:
    """Tests d'intégration avec la base de données"""

    def test_database_connection(self):
        """Vérifie la connexion à la base de données"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            assert cursor.fetchone()[0] == 1

    def test_complex_query_performance(self):
        """Test les performances des requêtes complexes"""
        # Création des données de test
        user = User.objects.create_user(username='dbtest', password='testpass123')
        post = Post.objects.create(
            title='Database Test',
            content='Content',
            author=user
        )
        
        # Création de commentaires
        for i in range(5):
            Comment.objects.create(
                post=post,
                author=user,
                content=f'Comment {i}'
            )

        # Test de requête avec jointures
        with CaptureQueriesContext(connection) as captured:
            result = Post.objects.select_related('author').prefetch_related('comments').get(pk=post.pk)
            assert result.title == 'Database Test'
            assert len(result.comments.all()) == 5
            assert len(captured.captured_queries) <= 3  # Maximum 3 requêtes
