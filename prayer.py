from urllib.request import urlopen
import json
import datetime


# ISSUES: Still no way to find region and country
# TODO: Should i include automatic date checking

CURRENT_TIME = 'http://api.aladhan.com/v1/currentTime?zone=Indian/Maldives'
GET_TIMINGS = 'http://api.aladhan.com/v1/calendar?latitude=5.410371&longitude=73.23074059999999&method=2&month=7&year=2019'
COORDINATES = 'http://ipinfo.io/'

def getCoordinate():
    locationData = parse_json(COORDINATES)['loc'].split(',')
    return locationData

def parse_json(url):
    json_data = {}
    try:
        response = urlopen(url)
        data = response.read().decode('utf-8')
        json_data = json.loads(data)
        return json_data

    except Exception as ex:
        print('Could not fetch data due to ', ex)

# Method is how the prayer is calculated, 3 is Muslim World League
def getPrayerData(month, year, method):
    latitude, longitude = getCoordinate()
    relevantPrayers = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    prayer_times = []
    URL = 'http://api.aladhan.com/v1/calendar?latitude={}&longitude={}&method={}&month={}&year={}'.format(latitude, longitude, method, month, year)
    json_data = parse_json(URL)
    date = datetime.datetime.today().day
    # date - 1 because the days are in 0 index in json result
    prayers = json_data['data'][date - 1]['timings']
    for key, value in prayers.items():
        if key in relevantPrayers:
            prayer_times.append(prayers[key])
        else:
            continue

    return prayer_times

def beautify(prayer_times):
    print('Date: ' + str(datetime.datetime.today()))
    for keys, values in prayer_times.items():
        print(keys + ': ', values.rjust(18))

# TODO: Clean up this function
def nextPrayer(prayer_times):
    prayers = []
    tDay = datetime.datetime.today()
    tHour = tDay.hour
    tMin = tDay.minute
    for k, v in prayer_times.items():
        pHour = int(v[0:2])
        pMin = int(v[3:5])
        lis = [pHour, pMin]
        prayers.append(lis)

    for prayer in prayers:
        nearest_difference = 99999
        difference = abs((prayer[0] - tHour + prayer[1] - tMin))
        if (difference) < nearest_difference:
            nearest_difference = difference
        print(nearest_difference)




print(getPrayerData(7, 2019, 3))
# print(beautify(getPrayerData(7, 2019, 3)))
# print(nextPrayer(getPrayerData(7, 2019, 2)))
# print(getCoordinate())
