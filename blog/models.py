from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

# Rôles utilisateur : admin, éditeur, lecteur
@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        lecteur_group, _ = Group.objects.get_or_create(name='lecteur')
        instance.groups.add(lecteur_group)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    is_draft = models.BooleanField(default=False, verbose_name="Brouillon")
    status = models.CharField(max_length=20, default='draft', verbose_name="Statut du post")

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_author = models.BooleanField(default=False, verbose_name="Mode auteur activé")
    status = models.CharField(max_length=100, blank=True, verbose_name="Statut/Humeur")
    notification_enabled = models.BooleanField(default=True, verbose_name="Notifications activées")

    def __str__(self):
        return self.user.username
