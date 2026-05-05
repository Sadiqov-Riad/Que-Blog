from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("/")

from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileForm
from apps.users.models import Profile

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("users:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=profile)
        
    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, "users/profile.html", context)


from django.core.exceptions import PermissionDenied

@login_required
def user_list_view(request):
    if request.user.role not in ['admin', 'superadmin']:
        raise PermissionDenied
        
    from apps.users.models import User as CustomUser
    # Exclude the superadmin from the list so they can't be modified/banned by regular admins
    users = CustomUser.objects.exclude(role='superadmin').order_by('-date_joined')
    return render(request, "users/user_list.html", {"users": users})

@login_required
def ban_user_view(request, user_id):
    if request.user.role not in ['admin', 'superadmin']:
        raise PermissionDenied
        
    from apps.users.models import User as CustomUser
    user = CustomUser.objects.get(id=user_id)
    if user.role == 'superadmin':
        raise PermissionDenied
        
    user.is_active = False
    user.save()
    return redirect('users:user_list')

@login_required
def unban_user_view(request, user_id):
    if request.user.role not in ['admin', 'superadmin']:
        raise PermissionDenied
        
    from apps.users.models import User as CustomUser
    user = CustomUser.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('users:user_list')

@login_required
def change_role_view(request, user_id, new_role):
    # ONLY superadmin can change roles
    if request.user.role != 'superadmin':
        raise PermissionDenied
        
    if new_role not in ['user', 'admin']:
        raise PermissionDenied
        
    from apps.users.models import User as CustomUser
    user = CustomUser.objects.get(id=user_id)
    if user.role == 'superadmin':
        raise PermissionDenied
        
    user.role = new_role
    user.save()
    return redirect('users:user_list')
