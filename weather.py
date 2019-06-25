#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import urllib.parse
import urllib.request

# weather's API
WEATHER_URL="http://weather.livedoor.com/forecast/webservice/json/v1?city=%s"
CITY_CODE="130010" # TOKYO
TODAY=0
TOMMOROW=1

# LINE notify's API
LINE_TOKEN="rKwhuZg8IgzvjS38YoK34ZfKmuC7C5fugIFUii3pg0J"
LINE_NOTIFY_URL="https://notify-api.line.me/api/notify"

def get_weather_info():
    try:
        url = WEATHER_URL % CITY_CODE
        html = urllib.request.urlopen(url) #URLを開く
        html_json = json.loads(html.read().decode('utf-8')) #json.loads() --> JSON文字列を辞書に変換, 
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)
    return html_json

def set_weather_info(weather_json, day):
    min_temperature = None
    max_temperature = None
    try:
        date = weather_json['forecasts'][day]['date']
        weather = weather_json['forecasts'][day]['telop']
        max_temperature = weather_json['forecasts'][day]['temperature']['max']['celsius']
        min_temperature = weather_json['forecasts'][day]['temperature']['min']['celsius']
    except TypeError:
        # temperature data is None etc...
        pass
    msg = "%s\nweather: %s\nmin: %s\nmax: %s" % \
               (date, weather, min_temperature, max_temperature)
    return msg

def send_weather_info(msg):
    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}
    payload = {"message": msg}
    try:
        payload = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)

def main():
    weather_json = get_weather_info()
    for day in [TODAY, TOMMOROW]:
        msg = set_weather_info(weather_json, day)
        send_weather_info(msg)

if __name__ == '__main__':
    main()