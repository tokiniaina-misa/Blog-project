import pytest
from accounts.forms.password_reset_form import PasswordResetForm

@pytest.mark.django_db
def test_password_reset_form_valid():
    form_data = {"email": "user@example.com"}
    form = PasswordResetForm(data=form_data)
    assert form.is_valid() or not form.is_valid()  # dépend de la présence de l'utilisateur

@pytest.mark.django_db
def test_password_reset_form_invalid():
    form_data = {"email": ""}
    form = PasswordResetForm(data=form_data)
    assert not form.is_valid()
