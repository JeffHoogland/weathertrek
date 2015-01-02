start_location = "Bloomington, IL"
end_location = "Columbus, OH"

daysout = 5

#Google Maps module
# https://github.com/swistakm/python-gmaps
import gmaps

#Weather module
# https://code.google.com/p/python-weather-api/
import pywapi

from gmaps import Directions
from gmaps import Geocoding

directions = Directions().directions(start_location, end_location)

directions = directions[0]

#holds the lat, lng of all the end points in our directions
positions = []

#holds the zipcodes of all the end points in our directions
zipcodes = []

for i in range(len(directions["legs"][0]["steps"])):
    positions.append(directions["legs"][0]["steps"][i]["end_location"])

#print positions

for pos in positions:
    results = Geocoding(sensor=False).reverse(lat=pos["lat"], lon=pos["lng"])
    for i in range(len(results[0]['address_components'])):
        if results[0]['address_components'][i]["types"][0] == "postal_code":
            if results[0]['address_components'][i]["short_name"] not in zipcodes:
                zipcodes.append(results[0]['address_components'][i]["short_name"])
            
print zipcodes

full_weather_y = []
full_weather_wc = []

for zippy in zipcodes:
    full_weather_y.append(pywapi.get_weather_from_yahoo(zippy))
    full_weather_wc.append(pywapi.get_weather_from_weather_com(zippy))


print "Yahoo weather report"
print ""
for cast in full_weather_y:
    #yahoo
    if "location" in cast:
        print "Location: %s"%cast["title"]
        print "Date: %s, %s"%(cast["forecasts"][daysout-1]["day"], cast["forecasts"][daysout-1]["date"])
        print "Forecast: %s"%(cast["forecasts"][daysout-1]["text"])
        print ""
    else:
        print cast
        print ""

'''print "Weather.com report"
print ""
for cast in full_weather_wc:
    #Weather.com prints
    print "Location: %s"%cast["location"]["name"]
    print "Date: %s, %s"%(cast["forecasts"][daysout-1]["day_of_week"], cast["forecasts"][daysout-1]["date"])
    print "Daytime: %s, %s percent chance of rain"%(cast["forecasts"][daysout-1]["day"]["text"], cast["forecasts"][daysout-1]["day"]["chance_precip"])
    print "Nighttime: %s, %s percent chance of rain"%(cast["forecasts"][daysout-1]["night"]["text"], cast["forecasts"][daysout-1]["night"]["chance_precip"])
    print ""
'''
