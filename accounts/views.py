from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('after_login_homepage')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def signup_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('after_login_homepage')

    return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Redirect to reset password form
            return redirect('accounts:reset_password', username=user.username)
        except User.DoesNotExist:
            messages.error(request, "No user found with that email address.")
    return render(request, 'forgot_password.html')

def reset_password(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect('accounts:forgot_password')

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful. Please log in with your new password.")
            return redirect('accounts:login')
    return render(request, 'reset_password.html', {'username': username})
