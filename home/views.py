from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.db.models import Count
from library import models as library_models
from . import forms


def home_page(request):
    most_borrowed_books = library_models.Book.objects.annotate(
    borrow_count=Count('borrowing')
).order_by('-borrow_count')[:10]
    
    return render(request, "library/home_page.html", {'books': most_borrowed_books})

def register_view(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect("home_page") 
    else:
        form = forms.RegisterForm()
    return render(request, "library/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home_page")
    else:
        form = forms.LoginForm()
    return render(request, "library/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home_page")