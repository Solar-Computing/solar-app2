from app.neurioclient import neurio_api
from enum import Enum
from flask import jsonify
from datetime import datetime
import pyowm


''' 
  logo categories:
    'logo'
    'goal'
    'trophy'
    'target'
    'light-bulb'
    'announcement'
'''
#format the data to be displayed on the API
def formatData(message, category=None, timestamp=None):
    if category not in ['logo', 'goal', 'trophy', 'target', 'light-bulb', 'announcement']: category = 'light-bulb'
    if not timestamp: timestamp = datetime.now().strftime("%b %-d %-I%p ET")
    return {"message" : message, "category" : category, "timestamp" : timestamp}


#main function to retrieve dictionaries of messages / logos / notification timestamps
def getFeedData():
    feedlist = []
    if getPeakForDailyData(): feedlist.append(formatData(getPeakForDailyData(), 'light-bulb'))
    if getDailyComparisonToPastMonth(): feedlist.append(formatData(getDailyComparisonToPastMonth(), 'target'))
    feedlist.append(formatData(getWeatherNotification(), 'logo'))
    return feedlist


#retrieve a message describing the peak for the day
def getPeakForDailyData():
    data = neurio_api.queryPastDay()
    if data:
        peak = max(data, key=lambda sample : sample["consumptionEnergy"])
        #time format: YYYY-MM-DDTHH:MM
        #return "Your peak energy consumption today was at " + ( datetime.strptime(peak["timestamp"][:16], "%Y-%m-%dT%H:%M") - timedelta(datetime.utcnow() + datetime.now()) ).strftime("%-I%p UTC")
        return "Your peak energy consumption today was at {}.".format(datetime.strptime(peak["timestamp"][:16], "%Y-%m-%dT%H:%M").strftime("%-I%p UTC"))
    return "No data found for today. Make sure to check your wifi connection."


#retrieve a message describing the daily consumption as compared to the monthly consumption
def getDailyComparisonToPastMonth():
    return "Your consumption is 10 percent below the average for the month... nice!"


#def retrieve a message giving advice based on the current weather
def getWeatherNotification():
    try:
        owm = pyowm.OWM('983cd71369086bf29f5f16b8438bf9fd')
        weather = owm.weather_at_place("Atlanta, US").get_weather()
        temperatures = weather.get_temperature('fahrenheit')

        #determine qualifier and write notification based on that
        if temperatures['temp_max'] > 70:
            if weather.get_clouds() < 30:
                return "It will be very sunny today, with a max temp of {} degrees F. Make sure to close your blinds to block out the heat!".format(temperatures['temp_max'])
            return "It will ve very hot today, with a max temp of {} degrees F".format(temperatures['temp_max'])
        elif temperatures['temp_min'] < 40:
            return "It will very very cold today, with a min temp of {} degrees F, so you probably won't need the AC today. Stay warm!".format(temperatures['temp_min'])
        return "It is currently {} degrees F and {}.".format(weather.get_status)
    
    except:
        return "We couldn't fetch the weather data right now, sorry.. check the weather online."
