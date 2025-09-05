# tests/test_forms.py

import pytest
from accounts.forms.register_form import RegisterForm

@pytest.mark.django_db
def test_register_form_valid():
    """
    Teste que le formulaire d'inscription est valide avec des données correctes.
    """
    form_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPass123",
        "password2": "StrongPass123"
    }
    form = RegisterForm(data=form_data)
    assert form.is_valid()

def test_register_form_password_mismatch():
    """
    Teste que le formulaire d'inscription détecte un mot de passe non concordant.
    """
    form_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPass123",
        "password2": "WrongPass123"
    }
    form = RegisterForm(data=form_data)
    assert not form.is_valid()
    assert "password2" in form.errors
