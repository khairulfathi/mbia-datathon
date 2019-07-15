import requests
import os
import calendar

if "WWOAPIKEY" not in os.environ:
    print("Config WWOAPIKEY missing")
    quit()

year = 2019
minmonth = 1
maxmonth = 1
endpoint = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"

#iterate between months
for month in range(minmonth, maxmonth + 1):

    #iterate through days of given month and year
    for day in range(1, calendar.monthrange(year, month)[1]):

        date = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
        query = {
            'key':os.environ['WWOAPIKEY'],
            'q':'40.490278,-74.2875',
            'date':date,
            'format':'json',
            'tp':1
            }

        req = requests.get(url = endpoint, params = query)
        data = req.json()

        for hourly in data['data']['weather'][0]['hourly']:
                print(date, hourly['time'], hourly['tempC'])
