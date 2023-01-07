from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

def user_logout(request):
    logout(request)
    return redirect("home")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request,"Email or password not correct")
    return render(request, 'login.html')

def user_register(request):
    pass