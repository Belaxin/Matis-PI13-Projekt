from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        # form.get_user() is from AuthenticationForm — already authenticated at this point
        login(request, form.get_user())
        return redirect("index")
    return render(request, "rezervacie/login.html", {"form": form})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)  # log them in immediately after registering
        messages.success(request, "Účet bol vytvorený.")
        return redirect("index")
    return render(request, "rezervacie/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
