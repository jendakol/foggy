#!/usr/bin/env python
import datetime
import json
import sys
from os import makedirs, chmod
from time import sleep
from zoneinfo import ZoneInfo

import dateutil
import requests
import dateutil.parser


def dew_point_coef(data):
    temp_diff = data["air_temperature"] - data["dew_point_temperature"]

    if temp_diff >= 4:
        return 0.1
    if temp_diff >= 3:
        return 0.2
    if temp_diff >= 2:
        return 0.4
    if temp_diff >= 1:
        return 0.8

    return 1


def humidity_coef(data):
    hum = data["relative_humidity"]

    if hum > 95:
        return 1
    if hum > 93:
        return 0.95

    return max(1.6 - (100 - hum) / 10.0, 0)  # 92 -> 0.8, 91 -> 0.7, 90 -> 0.6, ...


def wind_coef(data):
    wind = data["wind_speed"]

    if wind > 10:
        return 0.1
    if wind > 8:
        return 0.2
    if wind > 6:
        return 0.3
    if wind > 4:
        return 0.6
    if wind > 2:
        return 0.8
    if wind > 1:
        return 0.95

    return 1


def process_single(time_point):
    # print(data)
    details = time_point["data"]["instant"]["details"]
    time = dateutil.parser.isoparse(time_point["time"]).astimezone(ZoneInfo('Europe/Berlin'))

    prob = 1.0

    prob *= dew_point_coef(details)
    prob *= humidity_coef(details)
    prob *= wind_coef(details)

    return f"{time}: {prob * 100:.2f}%"


def forecast(now, dir, place):
    response_file = f"{dir}/response_{now}.json"
    forecast_file = f"{dir}/forecast_{now}.txt"
    webcam_file = f"{dir}/webcam_{now}.jpg"

    url = f'https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={place["lat"]}&lon={place["lon"]}'
    r = requests.get(url, headers={"user-agent": "foggy github.com/jendakol/foggy"}).json()

    series = r["properties"]["timeseries"]

    result = ""

    for time_point in series:
        result += process_single(time_point) + "\n"

    with open(response_file, "w", encoding='utf-8') as f:
        f.write(json.dumps(r))

    chmod(response_file, 0o666)

    with open(forecast_file, "w", encoding='utf-8') as f:
        f.write(result)

    chmod(forecast_file, 0o666)

    r = requests.get(place["webcam_link"], headers={"user-agent": "foggy github.com/jendakol/foggy"})
    with open(webcam_file, "wb") as f:
        f.write(r.content)

    chmod(webcam_file, 0o666)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Please provide path to places config")

    now = datetime.datetime.now().strftime("%Y%m%d-%H%M")

    places = json.loads(open(sys.argv[1], "r").read())

    for place in places:
        dir = f"/output/{place['dir']}/{now}"
        makedirs(dir, mode=0o777, exist_ok=True)
        chmod(dir, 0o777)  # sad but needed
        print(f"Processing {place['name']} into {dir}")
        forecast(now, dir, place)
        sleep(1)
