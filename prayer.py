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
    prayer_times = {}
    URL = 'http://api.aladhan.com/v1/calendar?latitude={}&longitude={}&method={}&month={}&year={}'.format(latitude, longitude, method, month, year)
    json_data = parse_json(URL)
    date = datetime.datetime.today().day
    # date - 1 because the days are in 0 index in json result

    # ISSUES: Sometimes get a none type
    prayers = json_data['data'][date - 1]['timings']

    for key, value in prayers.items():
        if key in relevantPrayers:
            prayer_times.setdefault(key, value[:5])
        else:
            continue

    return prayer_times

def beautify(prayer_times):
    print('Date: ' + str(datetime.datetime.today()))
    for keys, values in prayer_times.items():
        print(keys + ': ', values.rjust(18))


def findNearestPrayer(prayer_times):
    tHour = datetime.datetime.today().hour
    # All prayer data in a list cause i like lists
    prayers = []
    for k, v in prayer_times.items():
        prayers.append([k, int(v[:2]),int(v[3:])])

    # If next prayer is not fajr find out difference
    def findDifference(tHour):
        nearestDifference = 99999
        difference = 0
        nearestPrayer = ''
        possiblePrayers = []

        for prayer in prayers:
            if prayer[1] > tHour or prayer[1] == tHour:
                possiblePrayers.append(prayer)
        for prayer in possiblePrayers:
            difference = abs(tHour - prayer[1])
            if difference < nearestDifference:
                nearestDifference = difference
                nearestPrayer = prayer[0]

        return nearestPrayer


    if tHour > prayers[4][1] or tHour < prayers[0][1]:
        return prayers[0]

    return findDifference(tHour)



result = findNearestPrayer(getPrayerData(7, 2019, 2))
print(result)
