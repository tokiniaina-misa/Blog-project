from django import forms
from blog.models import Post

class DraftPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'categories', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'placeholder': 'Titre du brouillon',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'placeholder': 'Contenu du brouillon',
                'rows': 6,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border rounded',
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'w-full px-3 py-2 border rounded',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full px-3 py-2 border rounded',
            }),
        }
