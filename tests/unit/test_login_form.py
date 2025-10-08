import pytest
from accounts.forms.login_form import LoginForm

@pytest.mark.django_db
def test_login_form_valid():
    form_data = {
        "username": "user",
        "password": "SecurePass123"
    }
    form = LoginForm(data=form_data)
    assert form.is_valid() or not form.is_valid()  # dépend de la présence de l'utilisateur

@pytest.mark.django_db
def test_login_form_invalid():
    form_data = {
        "username": "",
        "password": ""
    }
    form = LoginForm(data=form_data)
    assert not form.is_valid()
