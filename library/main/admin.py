# pylint: skip-file
from django.contrib import admin
from .models import Author, Composition, Translation

admin.site.site_header = 'Библиотека переводов'

admin.site.register(Author)
admin.site.register(Composition)
admin.site.register(Translation)
