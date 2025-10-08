from django import forms
from blog.models import Post, Category, Tag


# Choix gaming fixes pour catégories et tags
CATEGORY_CHOICES = [
    ('RPG', 'RPG'),
    ('FPS', 'FPS'),
    ('Stratégie', 'Stratégie'),
    ('Indé', 'Indé'),
    ('Esport', 'Esport'),
    ('MMO', 'MMO'),
    ('Aventure', 'Aventure'),
    ('Simulation', 'Simulation'),
    ('Puzzle', 'Puzzle'),
    ('Plateforme', 'Plateforme'),
]
TAG_CHOICES = [
    ('review', 'review'),
    ('astuce', 'astuce'),
    ('guide', 'guide'),
    ('news', 'news'),
    ('multijoueur', 'multijoueur'),
    ('retro', 'retro'),
    ('PC', 'PC'),
    ('console', 'console'),
    ('speedrun', 'speedrun'),
    ('coop', 'coop'),
]

class PostForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mb-2 mr-4 accent-blue-600'}),
        label="Catégories (gaming)",
        required=True
    )
    tags = forms.MultipleChoiceField(
        choices=TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mb-2 mr-4 accent-green-600'}),
        label="Tags (gaming)",
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'categories', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'placeholder': 'Titre de l\'article',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'placeholder': 'Contenu de l\'article',
                'rows': 6,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'accept': 'image/*',
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Synchronise les catégories et tags avec les objets DB
        if commit:
            instance.save()
            # Catégories
            instance.categories.clear()
            for cat_name in self.cleaned_data['categories']:
                cat, _ = Category.objects.get_or_create(name=cat_name)
                instance.categories.add(cat)
            # Tags
            instance.tags.clear()
            for tag_name in self.cleaned_data['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        return instance
