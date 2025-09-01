from django import forms
from blog.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'is_author', 'status', 'notification_enabled']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'placeholder': 'Votre bio',
                'rows': 3,
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border rounded',
            }),
            'is_author': forms.CheckboxInput(attrs={
                'class': 'mr-2',
            }),
            'status': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'placeholder': 'Votre humeur ou statut',
            }),
            'notification_enabled': forms.CheckboxInput(attrs={
                'class': 'mr-2',
            }),
        }
