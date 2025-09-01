from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label=_('Nom d’utilisateur ou Email'),
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded',
            'placeholder': 'Nom d’utilisateur ou Email',
        })
    )
    password = forms.CharField(
        label=_('Mot de passe'),
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border rounded',
            'placeholder': 'Mot de passe',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')
        user = None
        if username_or_email and password:
            # Recherche par username ou email
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    pass
            if user is not None and user.check_password(password):
                if not user.is_active:
                    raise forms.ValidationError("Ce compte est inactif.")
                self.user_cache = user
            else:
                raise forms.ValidationError("Identifiants invalides.")
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)
