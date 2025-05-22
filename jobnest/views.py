from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'index.html')

def signup_page(request):
    return render(request, 'signup_page.html')

def login_page(request):
    return render(request, 'login_page.html')

@login_required
def after_login_homepage(request):
    return render(request, 'after_login_homepage.html')