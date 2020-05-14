# pylint: skip-file
from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^add_author/$', views.add_author, name='add_author'),
    url(r'^add_composition/$', views.add_composition, name='add_composition'),

    path('authors/<author_id>/show/', views.show_compositions, name='show_compositions'),
    path('authors/<author_id>/add/', views.add_translation, name='add_translation')
]
