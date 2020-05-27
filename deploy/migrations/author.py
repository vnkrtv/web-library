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
