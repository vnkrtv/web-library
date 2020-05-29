# pylint: disable=import-error, invalid-name, too-few-public-methods, relative-beyond-top-level
"""
Main app tests, covered views.py
"""
import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Composition, Translation


class MainTest(TestCase):
    """
    Base class for all tests
    """

    def setUp(self) -> None:
        """
        Add objects to temporary test database:
        - 'user' user
        """
        self.user = User.objects.create_user(
            id=1,
            username='user',
            password='top_secret')


class AuthorizationTest(MainTest):
    """
    Tests for authorization in the application
    """

    def test_successful_auth(self) -> None:
        """
        Test for successful authorization of users
        """
        client = Client()
        response = client.post(reverse('main:login_page'), {
            'username': self.user.username,
            'password': 'top_secret'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Выйти')

    def test_unsuccessful_auth(self) -> None:
        """
        Test for unsuccessful authorization of users
        """
        client = Client()
        response = client.post(reverse('main:login_page'), {
            'username': self.user.username,
            'password': 'wrong_password'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'неправильное имя пользователя или пароль!')


class RedirectTest(MainTest):
    """
    Tests for redirection in the application
    """

    def test_redirect(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        client = Client()
        response = client.post(reverse('main:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Войти в систему')


class MainPageTest(MainTest):
    """
    Tests for main page
    """

    def setUp(self) -> None:
        """
        Add objects to temporary test database:
        - 'user' user
        """
        super().setUp()
        Author.objects.create(
            id=20,
            name='First cool author',
            info='Bio text'
        )
        Author.objects.create(
            id=30,
            name='Second cool author',
            info='Bio text'
        )
        self.client = Client()
        self.client.post(reverse('main:login_page'), {
            'username': self.user.username,
            'password': 'top_secret'
        }, follow=True)

    def test_get_method(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.get(reverse('main:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First cool author')
        self.assertContains(response, 'Second cool author')

    def test_add_author_success(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:index'), {
            'add_author': ['Добавить'],
            'name': ['New author'],
            'info': ['New author bio'],
            'image': ['']
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First cool author')
        self.assertContains(response, 'Second cool author')
        self.assertContains(response, 'Автор New author был успешно добавлен в базу.')

        query = Author.objects.filter(name='New author')
        self.assertEqual(len(query), 1)

    def test_add_author_fail(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:index'), {
            'add_author': ['Добавить'],
            'name': ['New author'],
            'image': ['']
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First cool author')
        self.assertContains(response, 'Second cool author')
        self.assertContains(response, 'Форма некоректно заполнена.')

    def test_add_composition_success(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:index'), {
            'add_composition': ['Добавить'],
            'name': ['New composition'],
            'author': ['20'],
            'text': ['New composition text'],
            'lang': ['de']
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First cool author')
        self.assertContains(response, 'Second cool author')
        self.assertContains(response, 'New composition')
        self.assertContains(response, 'успешно добавлено')

        query = Composition.objects.filter(name='New composition')
        self.assertEqual(len(query), 1)

    def test_add_composition_fail(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:index'), {
            'add_composition': ['Добавить'],
            'name': ['New composition'],
            'author': ['20'],
            'text': ['New composition text'],
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First cool author')
        self.assertContains(response, 'Second cool author')
        self.assertContains(response, 'Форма некоректно заполнена.')


class CompositionsPageTest(MainTest):
    """
    Tests for compositions page
    """

    def setUp(self) -> None:
        """
        Add objects to temporary test database:
        - 'user' user
        """
        super().setUp()
        self.author = Author.objects.create(
            id=3,
            name='Cool author',
            info='Bio text'
        )
        Composition.objects.create(
            id=10,
            name='First composition',
            text='Text of first composition',
            author=self.author,
            lang='Немецкий'
        )
        Composition.objects.create(
            id=30,
            name='Second composition',
            text='Text of second composition',
            author=self.author,
            lang='Немецкий'
        )
        self.client = Client()
        self.client.post(reverse('main:login_page'), {
            'username': self.user.username,
            'password': 'top_secret'
        }, follow=True)

    def test_get_method(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.get(reverse('main:compositions', args=(self.author.id,)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First composition')
        self.assertContains(response, 'Second composition')

    def test_add_translation_success(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:compositions', args=(self.author.id,)), {
            'add_translation': ['Добавить'],
            'composition_id': ['10'],
            'text': ['Translation text'],
            'lang': ['de'],
            'author_id': ['1']
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First composition')
        self.assertContains(response, 'Second composition')
        self.assertContains(response, ' Перевод был успешно добавлен.')

        query = Translation.objects.filter(text='Translation text')
        self.assertEqual(len(query), 1)

    def test_add_translation_fail(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:compositions', args=(self.author.id,)), {
            'add_translation': ['Добавить'],
            'composition_id': ['10'],
            'text': [''],
            'lang': ['de'],
            'author_id': ['1']
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First composition')
        self.assertContains(response, 'Second composition')
        self.assertContains(response, 'Форма некоректно заполнена.')


class TranslationsPageTest(MainTest):
    """
    Tests for translations page
    """

    def setUp(self) -> None:
        """
        Add objects to temporary test database:
        - 'user' user
        """
        super().setUp()
        self.author = Author.objects.create(
            id=3,
            name='Cool author',
            info='Bio text'
        )
        self.composition = Composition.objects.create(
            id=10,
            name='First composition',
            text='Composition text in German',
            author=self.author,
            lang='Немецкий'
        )
        self.translation = Translation.objects.create(
            composition=self.composition,
            translation_author=self.user,
            text='Russian translation',
            lang='Русский'
        )
        Translation.objects.create(
            composition=self.composition,
            translation_author=self.user,
            text='French translation',
            lang='Французский'
        )
        self.client = Client()
        self.client.post(reverse('main:login_page'), {
            'username': self.user.username,
            'password': 'top_secret'
        }, follow=True)

    def test_get_method(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.get(reverse('main:translations', args=(self.composition.id,)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Русский')
        self.assertContains(response, 'Французский')
        self.assertContains(response, 'user')


class ShowTranslationPageTest(TranslationsPageTest):
    """
    Tests for show translation page
    """

    def test_get_method(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.get(reverse('main:show_translation', args=(self.translation.id,)), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Перевод')
        self.assertContains(response, self.translation.text)

        self.assertContains(response, 'Оригинал')
        self.assertContains(response, self.composition.text)


class SearchPageTest(TranslationsPageTest):
    """
    Tests for show translation page
    """

    def test_get_method(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.get(reverse('main:search'), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Добавить автора')
        self.assertContains(response, 'Добавить произведение')

    def test_search_success(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:search'), {
            'q': [self.composition.name]
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Результаты поиска')
        self.assertContains(response, f"По запросу '{self.composition.name}' были найдены следующие произведения:")
        self.assertContains(response, self.composition.name)

    def test_search_fail(self) -> None:
        """
        Tests for redirection of unauthenticated users
        """
        response = self.client.post(reverse('main:search'), {
            'q': ['Not found 404']
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Результаты поиска')
        self.assertContains(response, "Произведения по запросу 'Not found 404' не были найдены")
