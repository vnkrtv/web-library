from django.db import models


class Author(models.Model):
    name = models.CharField('Автор', max_length=100)
    info = models.TextField('Биография', default='')
    image = models.ImageField(upload_to='authors', default='authors/unnamed.jpg')

    def __repr__(self):
        return f'Author: {self.name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Composition(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор')
    name = models.CharField('Автор', max_length=100)

    def __repr__(self):
        return f'Composition: {self.name}'

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Translation(models.Model):
    LANGUAGES = [
        ('ru', 'Русский'),
        ('en', 'Английский'),
        ('de', 'Немецкий'),
        ('fr', 'Французский')
    ]
    composition = models.ForeignKey(
        Composition,
        on_delete=models.CASCADE,
        verbose_name='Произведение')
    text = models.TextField('Перевод')
    lang = models.CharField('Язык', max_length=100, choices=LANGUAGES)

    def __repr__(self):
        return f'Translation: {self.composition.name} on {self.lang}'

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'
