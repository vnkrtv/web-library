from django.db import models

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

    @staticmethod
    def get_names() -> list:
        return [(author.id, author.name) for author in Author.objects.all()]

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
