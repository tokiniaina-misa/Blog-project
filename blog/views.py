from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Comment, Category, Tag
from .forms import PostForm
from .forms_comment import CommentForm
from django.db.models import Q
from blog.models_notification import Notification
from django.http import JsonResponse

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'blog/notifications.html', {'notifications': notifications, 'notif_count': notif_count})

@login_required
def mark_notification_read(request, notif_id):
    notif = Notification.objects.get(id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('blog:notifications')

@staff_member_required
def admin_dashboard(request):
    nb_posts = Post.objects.count()
    nb_comments = Comment.objects.count()
    nb_users = User.objects.count()
    notif_count = 0
    if request.user.is_authenticated:
        notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'blog/admin_dashboard.html', {
        'nb_posts': nb_posts,
        'nb_comments': nb_comments,
        'nb_users': nb_users,
        'notif_count': notif_count,
    })

def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notif_count = 0
    if request.user.is_authenticated:
        notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query, 'notif_count': notif_count})

@login_required
def user_dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    liked_posts = request.user.liked_posts.all()
    comments = request.user.comments.all()
    notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'blog/dashboard.html', {
        'posts': posts,
        'liked_posts': liked_posts,
        'comments': comments,
        'notif_count': notif_count,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    if post.author != request.user:
        messages.error(request, "Vous ne pouvez supprimer que vos propres articles.")
        return redirect('blog:post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Article supprimé.")
        return redirect('blog:home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post, 'notif_count': notif_count})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    if post.author != request.user:
        messages.error(request, "Vous ne pouvez modifier que vos propres articles.")
        return redirect('blog:post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Article modifié.")
            return redirect('blog:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'notif_count': notif_count})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
        # Notification à l'auteur du post pour le like
        if post.author != request.user:
            from blog.models_notification import Notification
            Notification.objects.create(
                user=post.author,
                message=f"{request.user.username} a aimé votre article '{post.title}'",
                url=f"/post/{post.id}/"
            )
    return redirect('blog:post_detail', pk=pk)

@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
    return redirect('blog:post_detail', pk=pk)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            # Si une réponse à un commentaire
            parent_id = form.cleaned_data.get('parent')
            if parent_id:
                comment.parent = parent_id
            comment.save()
            # Notification à l'auteur du post ou du commentaire parent
            if comment.parent and comment.parent.author != request.user:
                from blog.models_notification import Notification
                Notification.objects.create(
                    user=comment.parent.author,
                    message=f"{request.user.username} a répondu à votre commentaire sur '{post.title}' : '{comment.content[:80]}{'...' if len(comment.content) > 80 else ''}'",
                    url=f"/post/{post.id}/#comment-{comment.id}"
                )
            elif post.author != request.user:
                from blog.models_notification import Notification
                Notification.objects.create(
                    user=post.author,
                    message=f"{request.user.username} a commenté votre article '{post.title}' : '{comment.content[:80]}{'...' if len(comment.content) > 80 else ''}'",
                    url=f"/post/{post.id}/#comment-{comment.id}"
                )
            messages.success(request, "Commentaire ajouté.")
        else:
            messages.error(request, "Erreur dans le commentaire.")
    return redirect('blog:post_detail', pk=pk)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    comment_form = CommentForm()
    is_liked = request.user.is_authenticated and post.likes.filter(id=request.user.id).exists()
    is_disliked = request.user.is_authenticated and post.dislikes.filter(id=request.user.id).exists()
    notif_count = 0
    if request.user.is_authenticated:
        notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'is_disliked': is_disliked,
        'notif_count': notif_count,
    })

from django.contrib.auth.decorators import login_required

@login_required
def post_create(request):
    notif_count = Notification.objects.filter(user=request.user, is_read=False).count()
    if not hasattr(request.user, 'profile') or not request.user.profile.is_author:
        messages.error(request, "Vous devez activer le mode auteur dans votre profil pour publier un article.")
        return redirect('blog:home')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # form.save_m2m() supprimé, la logique est dans PostForm.save()
            messages.success(request, "Article publié avec succès.")
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'notif_count': notif_count})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Category, Tag
from .forms import PostForm
from .forms_comment import CommentForm
from django.db.models import Q

def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.select_related('author').order_by('-created_at')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notif_count = 0
    if request.user.is_authenticated:
        notif_count = Notification.objects.filter(user=request.user, is_read=False).count()

    allowed_colors = ['blue','red','green','yellow','purple','pink','indigo','gray','orange','teal','cyan','lime','amber','emerald','fuchsia','rose']
    trending = []
    topics = []

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'query': query,
        'notif_count': notif_count,
        'allowed_colors': allowed_colors,
        'trending': trending,
        'topics': topics,
    })

@login_required
def notifications_json(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
    notif_list = [
        {
            'id': n.id,
            'message': n.message,
            'url': n.url,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%d/%m/%Y %H:%M'),
        }
        for n in notifications
    ]
    return JsonResponse({'notifications': notif_list})
