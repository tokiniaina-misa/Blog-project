from django.contrib.auth.decorators import login_required
from accounts.forms.profile_form import ProfileForm
from blog.models import Post, Profile
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import os

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Ensure avatar uploads are handled
        if form.is_valid():
            # Save the avatar to a specific subfolder
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                profile.avatar.save(os.path.join('avatars', avatar.name), avatar)
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    # Fetch user-specific metrics
    total_posts = Post.objects.filter(author=request.user).count()
    total_comments = Post.objects.filter(author=request.user).aggregate(total_comments=Count('comments'))['total_comments'] or 0
    total_likes = Post.objects.filter(author=request.user).aggregate(total_likes=Count('likes'))['total_likes'] or 0

    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'form': form,
        'posts': posts,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_likes': total_likes,
    })
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.forms.password_reset_form import CustomPasswordResetForm

def password_reset_request(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Réinitialisation de votre mot de passe"
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_url = request.build_absolute_uri(
                        reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    )
                    message = f"Cliquez sur ce lien pour réinitialiser votre mot de passe : {reset_url}"
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, "Si un compte existe avec cet email, un lien de réinitialisation a été envoyé.")
            return redirect('accounts:login')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre mot de passe a été réinitialisé. Vous pouvez vous connecter.")
                return redirect('accounts:login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
        return redirect('accounts:password_reset')
from django.contrib.auth import authenticate, login, logout
from accounts.forms.login_form import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect('blog:home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'show_navbar': False})

def logout_view(request):
    logout(request)
    messages.success(request, "Déconnexion réussie.")
    return redirect('accounts:login')
from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from accounts.forms.register_form import RegisterForm
from accounts.models import EmailVerificationToken

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            token = EmailVerificationToken.objects.create(user=user)
            verification_url = request.build_absolute_uri(
                reverse('accounts:verify_email', args=[str(token.token)])
            )
            send_mail(
                'Vérification de votre email',
                f'Cliquez sur ce lien pour vérifier votre compte : {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Un email de vérification a été envoyé. Veuillez vérifier votre boîte mail.")
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'show_navbar': False})

from django.http import HttpResponse
def verify_email(request, token):
    try:
        token_obj = EmailVerificationToken.objects.get(token=token, is_used=False)
        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.is_used = True
        token_obj.save()
        messages.success(request, "Votre email a été vérifié. Vous pouvez maintenant vous connecter.")
        return redirect('accounts:login')
    except EmailVerificationToken.DoesNotExist:
        return HttpResponse("Lien invalide ou déjà utilisé.")
