from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Пользователь')
    password = forms.PasswordInput()


class AuthorForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    info = forms.Te()

