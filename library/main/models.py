from django.db import models
from django.conf import settings

LANGUAGES = [
        ('ru', 'Русский'),
        ('en', 'Английский'),
        ('de', 'Немецкий'),
        ('fr', 'Французский')
    ]

class Author(models.Model):
    name = models.CharField('Автор', max_length=100)
    info = models.TextField('Биография', default='')
    image = models.ImageField(upload_to='authors', default='authors/unnamed.jpg')

    def __repr__(self):
        return f'<Author: {self.name}>'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Composition(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор')
    name = models.CharField('Автор', max_length=100)
    text = models.TextField('Оригинал', default='')
    lang = models.CharField('Язык оригинала', max_length=100, choices=LANGUAGES, default='ru')

    def __repr__(self):
        return f'<Composition: {self.name}>'

    def __str__(self):
        return self.name

    @staticmethod
    def get_by_author(author_id: int) -> list:
        return list(Composition.objects.filter(author__id=author_id))

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Translation(models.Model):
    composition = models.ForeignKey(
        Composition,
        on_delete=models.CASCADE,
        verbose_name='Произведение')
    translation_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор')
    text = models.TextField('Перевод')
    lang = models.CharField('Язык', max_length=100, choices=LANGUAGES, default='ru')

    def __repr__(self):
        return f'<Translation: {self.composition.name} on {self.lang}>'

    def __str__(self):
        return f'Перевод {self.composition.name} на {self.lang}, автор -  {self.translation_author}'

    @staticmethod
    def get_by_composition(composition_id: int) -> list:
        return list(Translation.objects.filter(composition__id=composition_id))

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'
