from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user
from .models import Author, Composition, Translation
from .forms import AuthorForm, CompositionForm, TranslationForm


class IndexView(View):
    template = 'main/main.html'
    title = 'Главная страница | Библиотека'
    context = {}

    @method_decorator(unauthenticated_user)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def add_author(self):
        author_form = self.context['author_form']
        if author_form.is_valid():
            name = author_form.cleaned_data["name"]
            Author.objects.create(
                name=name,
                info=author_form.cleaned_data["info"],
                image=author_form.cleaned_data["image"])
            self.context['success'] = f'Автор {name} был успешно добавлен в базу.'
        else:
            self.context['error'] = 'Форма некоректно заполнена.'

    def add_composition(self):
        comp_form = self.context['comp_form']
        if comp_form.is_valid():
            name = comp_form.cleaned_data["name"]
            Composition.objects.create(
                author=comp_form.cleaned_data["author"],
                name=name,
                text=comp_form.cleaned_data["text"],
                lang=comp_form.get_lang())
            self.context['success'] = f"Произведение '{name}' было успешно добавлено в базу."
        else:
            self.context['error'] = 'Форма некоректно заполнена.'

    def get(self, request):
        self.context = {
            'title': self.title,
            'authors': Author.objects.all(),
            'author_form': AuthorForm(),
            'comp_form': CompositionForm()
        }
        return render(request, self.template, self.context)

    def post(self, request):
        self.context = {
            'title': self.title,
            'authors': Author.objects.all(),
            'author_form': AuthorForm(request.POST, request.FILES),
            'comp_form': CompositionForm(request.POST)
        }
        if 'add_author' in request.POST:
            self.add_author()
        if 'add_composition' in request.POST:
            self.add_composition()
        return render(request, self.template, self.context)


class CompositionsView(View):
    template = 'main/compositions.html'
    title = 'Главная страница | Библиотека'
    context = {}

    @method_decorator(unauthenticated_user)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def add_translation(self, request):
        form = self.context['form']
        if form.is_valid():
            composition = Composition.objects.get(id=request.POST['composition_id'])
            author = User.objects.get(id=request.POST['author_id'])
            Translation.objects.create(
                composition=composition,
                text=form.cleaned_data["text"],
                translation_author=author,
                lang=form.get_lang())
            self.context['success'] = 'Перевод был успешно добавлен.'
        else:
            self.context['error'] = 'Форма некоректно заполнена.'

    def get(self, request, author_id):
        form = TranslationForm()
        self.context = {
            'title': f'{Author.objects.get(id=author_id)} | Библиотека',
            'compositions': Composition.get_by_author(author_id),
            'author': Author.objects.get(id=author_id),
            'form': form
        }
        return render(request, self.template, self.context)

    def post(self, request, author_id):
        form = TranslationForm(request.POST)
        self.context = {
            'title': f'{Author.objects.get(id=author_id)} | Библиотека',
            'compositions': Composition.get_by_author(author_id),
            'author': Author.objects.get(id=author_id),
            'form': form
        }
        if 'add_translation' in request.POST:
            self.add_translation(request)
        return render(request, self.template, self.context)


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
def search(request):
    if request.method == "POST":
        q = request.POST['q']
        context = {
            'title': 'Результаты поиска | Библиотека',
            'compositions': Composition.objects.filter(name__contains=q),
            'q': q
        }
        return render(request, 'main/search.html', context)

    return redirect('/')


@unauthenticated_user
def translations(request, composition_id):
    context = {
        'title': 'Переводы | Библиотека',
        'translations': Translation.get_by_composition(composition_id),
        'composition': Composition.objects.get(id=composition_id)
    }
    return render(request, 'main/translations.html', context)


@unauthenticated_user
def show_translation(request, translation_id):
    translation = Translation.objects.get(id=translation_id)
    context = {
        'title': 'Перевод | Библиотека',
        'translation': translation,
    }
    return render(request, 'main/show_translation.html', context)
