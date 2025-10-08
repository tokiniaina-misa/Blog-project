from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Page d'accueil (liste des posts)
    path('', views.post_list, name='home'),
    path('posts/', views.post_list, name='post_list'),
    # CRUD posts
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    # Commentaires
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    # Likes/Dislikes
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/dislike/', views.dislike_post, name='dislike_post'),
    # Recherche
    path('search/', views.search, name='search'),
    # Dashboard utilisateur
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/<int:notif_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/json/', views.notifications_json, name='notifications_json'),
]
