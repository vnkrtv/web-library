from django import forms
from .models import LANGUAGES, Author


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name != 'image':
                visible.field.widget.attrs['class'] = 'form-control'


class AuthorForm(BaseForm):
    name = forms.CharField(label='Имя', max_length=100)
    info = forms.CharField(label='Справка', widget=forms.Textarea)
    image = forms.ImageField(label='Фотография', required=False)


class CompositionForm(BaseForm):
    author = forms.ModelChoiceField(label='Автор', queryset=Author.objects.all())
    name = forms.CharField(label='Название')
    text = forms.CharField(label='Оригинал', widget=forms.Textarea)
    lang = forms.ChoiceField(label='Язык оригинала', choices=LANGUAGES)

    def get_author(self):
        return Author.objects.get(id=int(self.cleaned_data['author']))

    def get_lang(self):
        lang_dict = dict(LANGUAGES)
        return lang_dict[self.cleaned_data['lang']]


class TranslationForm(BaseForm):
    text = forms.CharField(label='Текст перевода', widget=forms.Textarea)
    lang = forms.ChoiceField(label='Язык перевода', choices=LANGUAGES)

    def get_lang(self):
        lang_dict = dict(LANGUAGES)
        return lang_dict[self.cleaned_data['lang']]
