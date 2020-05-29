# pylint: skip-file
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^search/$', views.search, name='search'),

    path('authors/<author_id>/', views.CompositionsView.as_view(), name='compositions'),
    path('composition/<composition_id>', views.translations, name='translations'),
    path('translation/<translation_id>', views.show_translation, name='show_translation'),
]
