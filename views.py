from . import weather
from . import league
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
        return HttpResponse("Hello, World!")

def austin_weather(request):
        return weather.get_current_weather()

def league_stuff(request):
        return league.try_this()
