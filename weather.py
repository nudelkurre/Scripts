#!/usr/bin/env python3

import requests
import argparse
import re
from datetime import datetime

weatherCodes = {
    "113": "Sunny",
    "116": "PartlyCloudy",
    "119": "Cloudy",
    "122": "VeryCloudy",
    "143": "Fog",
    "176": "LightShowers",
    "179": "LightSleetShowers",
    "182": "LightSleet",
    "185": "LightSleet",
    "200": "ThunderyShowers",
    "227": "LightSnow",
    "230": "HeavySnow",
    "248": "Fog",
    "260": "Fog",
    "263": "LightShowers",
    "266": "LightRain",
    "281": "LightSleet",
    "284": "LightSleet",
    "293": "LightRain",
    "296": "LightRain",
    "299": "HeavyShowers",
    "302": "HeavyRain",
    "305": "HeavyShowers",
    "308": "HeavyRain",
    "311": "LightSleet",
    "314": "LightSleet",
    "317": "LightSleet",
    "320": "LightSnow",
    "323": "LightSnowShowers",
    "326": "LightSnowShowers",
    "329": "HeavySnow",
    "332": "HeavySnow",
    "335": "HeavySnowShowers",
    "338": "HeavySnow",
    "350": "LightSleet",
    "353": "LightShowers",
    "356": "HeavyShowers",
    "359": "HeavyRain",
    "362": "LightSleetShowers",
    "365": "LightSleetShowers",
    "368": "LightSnowShowers",
    "371": "HeavySnowShowers",
    "374": "LightSleetShowers",
    "377": "LightSleet",
    "386": "ThunderyShowers",
    "389": "ThunderyHeavyRain",
    "392": "ThunderySnowShowers",
    "395": "HeavySnowShowers",
}

weatherSymbol = {
    "Unknown":             "?",
    "Cloudy":              "",
    "Fog":                 "",
    "HeavyRain":           "",
    "HeavyShowers":        "",
    "HeavySnow":           "",
    "HeavySnowShowers":    "",
    "LightRain":           "",
    "LightShowers":        "",
    "LightSleet":          "",
    "LightSleetShowers":   "",
    "LightSnow":           "",
    "LightSnowShowers":    "",
    "PartlyCloudy":        "",
    "Sunny":               "",
    "ThunderyHeavyRain":   "",
    "ThunderyShowers":     "",
    "ThunderySnowShowers": "",
    "VeryCloudy": "",
}

parser = argparse.ArgumentParser(prog="Weather", formatter_class=argparse.RawDescriptionHelpFormatter, description="""Get weather data from location

Valid values for STRING_FORMAT is:
    {tempC}:       Get current temperature in celsius
    {fellsLikeC}   Get what temperature it feels like
    {cloudcover}    Get the current cloud cover
    {humidity}      Get current humidity
    {precipMM}      Get precipitation
    {pressure}      Get current pressure
    {uvIndex}       Get current UV index
    {visibility}    Get visibility in kilometers
    {weatherIcon}   Get symbol of current weather
    {weatherDesc}   Get short description of current weather
    {windspeed}     Get current windspeed in kph
    {windspeedms}   Get current windspeed in ms
    {sunrise}       Get time for sunrise
    {sunset}        Get time for sunset
""")
parser.add_argument(dest="location", help="Enter location for weatherdata")
parser.add_argument("-f", dest="string_format", default="{location}: {weatherIcon} {tempC}", help="Format output of string (default: {location}: {weatherIcon} {tempC})")
args = parser.parse_args()

def parseString(weatherstring, data):
    tokens = re.compile(r"\{\w+\}")
    res = tokens.findall(weatherstring)
    for i in res:
        token = i[1:-1]
        if(token in data):
            weatherstring = weatherstring.replace(i, data[token])
    return weatherstring

def kphToMs(kph):
    fl = re.compile(r"^[0-9]+\.[0-9]*$|^[0-9]+$")
    res = re.match(fl, kph)
    if(res):
        float_parts = str(float(kph) / 3.6).split(".")
        if(len(float_parts) > 1):
            float_parts[1] = float_parts[1][0:1]
        return ".".join(float_parts)
    raise TypeError(f"Value of kph is not valid float (value: {kph})")

def convert24(timestr):
    timestr_split = timestr.split(" ")
    time = timestr_split[0]
    time = time.split(":")
    ampm = timestr_split[1].lower()
    if(ampm == "pm"):
        time[0] = str(int(time[0]) + 12)
        return ":".join(time)
    elif(ampm == "am"):
        return ":".join(time)

def convertCode(code):
    if(code in weatherCodes):
        return weatherSymbol[weatherCodes[code]]
    return weatherSymbol["Unknown"]

url = f"https://wttr.in/{args.location}"
params = {"format": "j1", "lang": "sv"}

res = requests.get(url, params).json()
weather = res['current_condition'][0]
sundata = res['weather'][0]['astronomy'][0]
weatherdata = {
    "location": args.location,
    "tempC": f"{weather['temp_C']}°C",
    "fellsLikeC": weather['FeelsLikeC'],
    "cloudcover": weather['cloudcover'],
    "humidity": weather['humidity'],
    "precipMM": weather['precipMM'],
    "pressure": weather['pressure'],
    "uvIndex": weather['uvIndex'],
    "visibility": weather['visibility'],
    "weatherIcon": convertCode(weather['weatherCode']),
    "weatherDesc": weather['weatherDesc'][0]['value'],
    "windspeed": weather['windspeedKmph'],
    "windspeedms": kphToMs(weather['windspeedKmph']),
    "sunrise": convert24(sundata['sunrise']),
    "sunset": convert24(sundata['sunset']),
}

print(parseString(args.string_format, weatherdata))
