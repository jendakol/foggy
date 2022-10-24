import json
import sys
from zoneinfo import ZoneInfo

import dateutil
import requests
import dateutil.parser

lat = 50.5409239
lon = 13.9374158


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


def process_single(data):
    # print(data)
    details = data["data"]["instant"]["details"]
    time = dateutil.parser.isoparse(data["time"]).astimezone(ZoneInfo('Europe/Berlin'))

    prob = 1.0

    prob *= dew_point_coef(details)
    prob *= humidity_coef(details)
    prob *= wind_coef(details)

    print(f"{time}: {prob * 100:.2f}%")


def forecast():
    if len(sys.argv) == 2:
        r = json.loads(open(sys.argv[1], "r").read())
    else:
        url = f'https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={lat}&lon={lon}'
        r = requests.get(url, headers={"user-agent": "foggy github.com/jendakol/foggy"}).json()

    series = r["properties"]["timeseries"]

    for data in series:
        process_single(data)


if __name__ == '__main__':
    forecast()
