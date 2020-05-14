from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from .models import Author, Composition, Translation


def login_page(request):
    """
    In case of successful authorization redirect to get_tests page, else displays login page with error
    """
    logout(request)
    if 'username' not in request.POST or 'password' not in request.POST:
        return render(request, 'main/login.html')
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'main/login.html', {'error': 'Ошибка: аккаунт пользователя отключен!'})
    else:
        return render(request, 'main/login.html', {'error': 'Ошибка: неправильное имя пользователя или пароль!'})


@unauthenticated_user
def index(request):
    info = {
        'title': 'Главная страница | Библиотека',
        'authors':  Author.objects.all()
    }
    return render(request, 'main/main.html', info)
