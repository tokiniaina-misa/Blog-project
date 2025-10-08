import pytest
from django.test import RequestFactory
from accounts.middleware import LoginRequiredMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest

@pytest.mark.django_db
def test_middleware_redirect_if_not_authenticated():
    factory = RequestFactory()
    request = factory.get('/accounts/profile/')
    request.user = AnonymousUser()
    middleware = LoginRequiredMiddleware(lambda req: None)
    response = middleware(request)
    # Doit rediriger vers la page de login
    assert hasattr(response, 'status_code')
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
def test_middleware_no_redirect_if_authenticated():
    factory = RequestFactory()
    request = factory.get('/accounts/profile/')
    user = User.objects.create_user(username='testuser', password='pass')
    request.user = user
    middleware = LoginRequiredMiddleware(lambda req: 'ok')
    response = middleware(request)
    assert response == 'ok'
