#!/usr/bin/python
# -*- coding: utf-8 -*-

# These are the items that can be customized for a different location.
# The zipcode is just the 5-digit code; no need for extensions.
# The station can be found by going to 
#   http://www.weather.gov/xml/current_obs/seek.php?state=il&Find=Find
# and choosing the closest NOAA station for your state.
# The radar image can be found at http://weather.com by searching
# on your location and then following the "Classic Map" link. Use
# the URL of that image here.
zipcode = '60502'
station = 'KARR'
radar   = 'http://i.imwx.com/web/radar/us_ord_ultraradar_plus_usen.jpg'


# The code below shouldn't be modified unless you want to change the layout
# or the type of data presented.

import pywapi
import datetime
import re

# import cgitb
# cgitb.enable()

# The date and time as a string. Note: My host's server is on Eastern Time
# and I'm on Central Time, so I subtract an hour.
now = datetime.datetime.now() - datetime.timedelta(hours=1)
now = now.strftime("%a, %b %d %I:%M %p")
# Delete leading zeros for day and hour.
now = re.sub(r' 0(\d )', r' \1', now)   # day has a space before and after
now = re.sub(r'0(\d:)', r'\1', now)     # hour has a colon after

# Get the current conditions for the given station.
noaa = pywapi.get_weather_from_noaa(station)
yahoo = pywapi.get_weather_from_yahoo(zipcode, '')

# Interpretation of the Yahoo pressure dictionary.
ypressure = {'0': 'steady', '1': 'rising', '2': 'falling'}

# Check for gusts.
try:
  gust = ', gusting to %s mph' % noaa['wind_gust_mph']
except KeyError:
  gust = ''
  
# The forecasts
today = yahoo['forecasts'][0]
tomorrow = yahoo['forecasts'][1]

# Assemble the content,.
content = '''Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta name="viewport" content = "width = device-width" />
<title>Weather - %s</title>
<style type="text/css">
  body { font-family: Helvetica;}
  h1 { font-size: 125%%;}
</style>
</head>
<body>
<h1>Temperature: %.0f&deg;</h1>
<p>%s<br />
Wind: %s at %s mph%s<br />''' % (now, float(noaa['temp_f']), yahoo['condition']['text'], noaa['wind_dir'], noaa['wind_mph'], gust )

try:
  content += 'Wind Chill: %s&deg;<br />\n' % noaa['windchill_f']
except KeyError:
  pass

content += 'Relative Humidity: %s%%<br />\n' % noaa['relative_humidity']

try:
  content += 'Heat Index: %s&deg;<br />\n' % noaa['heat_index_f']
except KeyError:
  pass

content += 'Pressure: %s and %s<br />\n' % (float(yahoo['atmosphere']['pressure']), ypressure[yahoo['atmosphere']['rising']])

content += 'Sunlight: %s to %s</p>\n' % (yahoo['astronomy']['sunrise'], yahoo['astronomy']['sunset'])

content += '<p><img width="100%%" src="%s" /></p>\n' % radar

content += '''<h1>Today</h1>
<p>High: %s&deg;<br />
Low: %s&deg;<br />
%s</p>
''' % (int(today['high']), int(today['low']), today['text'])

content += '''<h1>Tomorrow</h1>
<p>High: %s&deg;<br />
Low: %s&deg;<br />
%s</p>
''' % (int(tomorrow['high']), int(tomorrow['low']), tomorrow['text'])

content += '''</body>
</html>'''

print content.encode('utf8')

