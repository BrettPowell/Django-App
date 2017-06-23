import os
import requests
from . import config

from django.http import HttpResponse

def get_current_weather():
    current_weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Austin,US&units=imperial&APPID={}".format(os.environ.get('Weather_Key'))).json()
    five_day = requests.get("http://api.openweathermap.org/data/2.5/forecast?zip=78758,US&units=imperial&APPID={}".format(os.environ.get('Weather_Key'))).json()
    # Max and min are just the range of the area you ask for. Depeding on the location temps can
    # vary in a small area.
    #{'humidity': 61, 'pressure': 1016, 'temp_max': 84.2, 'temp_min': 80.6, 'temp': 82.4}
    temp_five = [five_day['list'][i]['main']['temp'] for i in range(5)]
    x = '''
<html>
<head>
<style>
body {
  background: #333;
  color: #fff;
  font-family: monospace;
  padding-top: 5em;
  display: flex;
  justify-content: center;
}

/* DEMO-SPECIFIC STYLES */
.typewriter h1 {
  overflow: hidden; /* Ensures the content is not revealed until the animation */
  border-right: .15em solid orange; /* The typwriter cursor */
  white-space: nowrap; /* Keeps the content on a single line */
  margin: 0 auto; /* Gives that scrolling effect as the typing happens */
  letter-spacing: .15em; /* Adjust as needed */
  animation:
    typing 3.5s steps(40, end),
    blink-caret .75s step-end infinite;
}

/* The typing effect */
@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}

/* The typewriter cursor effect */
@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: orange; }
}

</style>
</head>
'''
    for i in range(len(temp_five)):
        x += ' '
        x += str(temp_five[i])
    x += '</head><body>'
    html = """<div class='typewriter'> <h1> Current Tempature is {} </h1></div>
         <body>Next 5 Days: {}</body>""".format(current_weather['main']['temp'], x)
    return HttpResponse(html)
