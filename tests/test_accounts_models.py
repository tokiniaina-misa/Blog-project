import pytest
from accounts.models import EmailVerificationToken
from django.contrib.auth import get_user_model
import uuid

@pytest.mark.django_db
def test_email_verification_token_str():
    user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='pass')
    token_uuid = uuid.uuid4()
    token = EmailVerificationToken.objects.create(user=user, token=token_uuid)
    assert str(token.token) == str(token_uuid)
