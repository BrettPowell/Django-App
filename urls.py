from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^weather$', views.austin_weather, name='Current Weather'),
    url(r'^lol$', views.league_stuff, name='League'),
]
