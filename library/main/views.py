from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .decorators import unauthenticated_user
from .models import Author, Composition, Translation
from .forms import AuthorForm, CompositionForm, TranslationForm


def login_page(request):
    """
    In case of successful authorization redirect to get_tests page, else displays login page with error
    """
    logout(request)
    if 'username' not in request.POST or 'password' not in request.POST:
        return render(request, 'main/login.html')
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password'])
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


@unauthenticated_user
def search(request):
    if request.method == "POST":
        q = request.POST['q']
        info = {
            'title': 'Результаты поиска | Библиотека',
            'compositions': Composition.objects.filter(name__contains=q),
            'q': q
        }
        return render(request, 'main/search.html', info)

    return redirect('/')


@unauthenticated_user
def add_author(request):
    info = {
        'title': 'Добавить автора | Библиотека',
    }
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            author = Author.objects.create(
                name=name,
                info=form.cleaned_data["info"],
                image=form.cleaned_data["image"])
            author.save()
            info['success'] = f'Автор {name} был успешно добавлен в базу.'
        else:
            info['error'] = 'Форма некоректно заполнена.'
    else:
        form = AuthorForm()
    info['form'] = form
    return render(request, 'main/add_author.html', info)


@unauthenticated_user
def add_composition(request):
    info = {
        'title': 'Добавить произведение | Библиотека',
    }
    if request.method == "POST":
        form = CompositionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            composition = Composition.objects.create(
                author=form.get_author(),
                name=name,
                text=form.cleaned_data["text"],
                lang=form.get_lang())
            composition.save()
            info['success'] = f"Произведение '{name}' было успешно добавлен в базу."
        else:
            info['error'] = 'Форма некоректно заполнена.'
    else:
        form = CompositionForm()
    info['form'] = form
    return render(request, 'main/add_composition.html', info)


@unauthenticated_user
def show_compositions(request, author_id):
    info = {
        'title': f'{Author.objects.get(id=author_id)} | Библиотека',
        'compositions': Composition.get_by_author(author_id),
        'author': Author.objects.get(id=author_id)
    }
    return render(request, 'main/show_compositions.html', info)


@unauthenticated_user
def add_translation(request, composition_id):
    composition = Composition.objects.get(id=composition_id)
    info = {
        'title': 'Добавить перевод | Библиотека',
        'composition': composition
    }
    if request.method == "POST":
        form = TranslationForm(request.POST)
        if form.is_valid():
            translation = Translation.objects.create(
                composition=composition,
                text=form.cleaned_data["text"],
                translation_author=form.cleaned_data["translation_author"],
                lang=form.get_lang())
            translation.save()
            info['success'] = 'Перевод был успешно добавлен.'
        else:
            info['error'] = 'Форма некоректно заполнена.'
    else:
        form = TranslationForm()
        form.fields["translation_author"].initial = request.user.username
    info['form'] = form
    return render(request, 'main/add_translation.html', info)


@unauthenticated_user
def show_translations(request, composition_id):
    info = {
        'title': 'Переводы | Библиотека',
        'translations': Translation.get_by_composition(composition_id),
        'composition': Composition.objects.get(id=composition_id)
    }
    return render(request, 'main/show_translations.html', info)


@unauthenticated_user
def show_translation(request, translation_id):
    translation = Translation.objects.get(id=translation_id)
    info = {
        'title': 'Перевод | Библиотека',
        'translation': translation,
        'composition': translation.composition
    }
    return render(request, 'main/show_translation.html', info)
