from django import forms
from .models import LANGUAGES, Author, Composition


class AuthorForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100, required=True)
    info = forms.CharField(label='Справка', widget=forms.Textarea)
    image = forms.ImageField(label='Фотография')


class CompositionForm(forms.Form):
    author = forms.ChoiceField(label='Автор', choices=Author.get_names())
    name = forms.CharField(label='Название')
    text = forms.CharField(label='Оригинал', widget=forms.Textarea)
    lang = forms.ChoiceField(label='Язык оригинала', choices=LANGUAGES)

    def get_author(self):
        return Author.objects.get(id=int(self.cleaned_data['author']))

    def get_lang(self):
        lang_dict = dict(LANGUAGES)
        return lang_dict[self.cleaned_data['lang']]


class TranslationForm(forms.Form):
    translation_author = forms.CharField(label='Автор перевода')
    composition = forms.ChoiceField(label='Произведение')
    text = forms.CharField(label='Текст перевода', widget=forms.Textarea)
    lang = forms.ChoiceField(label='Язык перевода', choices=LANGUAGES)

    def get_composition(self):
        return Author.objects.get(id=int(self.cleaned_data['composition']))

    def get_lang(self):
        lang_dict = dict(LANGUAGES)
        return lang_dict[self.cleaned_data['lang']]
