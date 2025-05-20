from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

def signup_page(request):
    return render(request, 'signup_page.html')

def login_page(request):
    return render(request, 'login_page.html')

def after_login(request):
    return render(request, 'after_login.html')