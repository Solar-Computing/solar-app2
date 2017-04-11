import app.controllers.notificationcache as notificationcache
from app.neurioclient import neurio_api
from enum import Enum
from flask import jsonify
from datetime import datetime, timedelta
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
def formatData(n_type, message, category=None, timestamp=None):
    if category not in ['logo', 'goal', 'trophy', 'target', 'light-bulb', 'announcement']: category = 'light-bulb'
    if not timestamp: timestamp = datetime.now() #.strftime("%b %-d %-I%p ET")
    return {"type" : n_type, "message" : message, "category" : category, "timestamp" : timestamp}

#main function to retrieve dictionaries of messages / categories / notification timestamps
#turn notification timestamps into strings to be displayed as json objects
def getFeedData():

    #TODO if dailyPeak now at a new high, post new message 
    if not notificationcache.notificationInLastInterval("dailyPeak", timedelta(minutes=2)):
        notificationcache.addNotification(formatData("dailyPeak", getPeakForDailyData()))

    #TODO if weather hasn't had notification in past 2 hours, post another one
    if not notificationcache.notificationInLastInterval("weather", timedelta(minutes=1)):
        notificationcache.addNotification(formatData("weather", getWeatherNotification()))

    #TODO post average daily
    if not notificationcache.notificationInLastInterval("dailyCompToMonth", timedelta(minutes=4)):
        notificationcache.addNotification(formatData("dailyCompToMonth", getDailyComparisonToPastMonth()))

    return notificationcache.getNotifications()



# -------------------- message generation logic --------------------

#retrieve a message describing the peak for the day
def getPeakForDailyData():
    data = neurio_api.queryPastDay()
    if data:
        peak = max(data, key=lambda sample : sample["consumptionEnergy"])
        #time format: YYYY-MM-DDTHH:MM
        #return "Your peak energy consumption today was at " + ( datetime.strptime(peak["timestamp"][:16], "%Y-%m-%dT%H:%M") - timedelta(datetime.utcnow() + datetime.now()) ).strftime("%-I%p UTC")
        return "Your peak energy consumption today was at {}.".format(datetime.strptime(peak["timestamp"][:16], "%Y-%m-%dT%H:%M").strftime("%-I%p UTC"))
    return "dailyPeak", "No data found for today. Make sure to check your wifi connection."


#retrieve a message describing the daily consumption as compared to the monthly consumption
def getDailyComparisonToPastMonth():

    #data retrieval
    samples_month = [sample['consumptionEnergy'] for sample in neurio_api.queryPastMonth()]
    average_month = sum(samples_month) / len(samples_month)
    samples_today = [sample['consumptionEnergy'] for sample in neurio_api.queryPastDay()]
    average_today = sum(samples_today) / len(samples_today)

    #message logic
    if abs(average_month - average_today) < 100: return "Your consumptions is right on par with the monthly average today."
    elif average_today < average_month: return "Good work! Your consumption is {}%  below the average for the month!".format( round((average_month-average_today)/average_month, 1) )
    else: return "Hey.. your consumption is higher today than the average for this month by {}%. Make sure to turn off anything you're not using.".format( round((average_today-average_month)/average_month, 1) ) 


#retrieve a message giving advice based on the current weather
def getWeatherNotification():
    try:
        #API calls for data retrieval
        owm = pyowm.OWM('983cd71369086bf29f5f16b8438bf9fd')
        weather = owm.weather_at_place("Atlanta, US").get_weather()
        temperatures = weather.get_temperature('fahrenheit')

        #notification logic based on weather qualifiers
        if temperatures['temp_max'] > 70:
            if weather.get_clouds() < 30:
                return "It will be very sunny today, with a max temp of {} degrees F. Make sure to close your blinds to block out the heat!".format(temperatures['temp_max'])
            return "It will ve very hot today, with a max temp of {} degrees F".format(temperatures['temp_max'])
        elif temperatures['temp_min'] < 40:
            return "It will very cold today or tonight, with a min temp of {} degrees F, so you probably won't need the AC today. Stay warm!".format(temperatures['temp_min'])
        return "It is currently {} degrees F and {}.".format(temperatures['temp'], weather.get_status().lower())

    except:
        return "We couldn't fetch the weather data right now, sorry.. check the weather online."
