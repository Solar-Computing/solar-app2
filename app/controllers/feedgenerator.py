import app.controllers.notificationcache as notificationcache
from datetime import datetime, timedelta
from app.neurioclient import neurio_api
from flask import jsonify
from enum import Enum
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
    if category not in ['Notification', 'Warning', 'Congratulations', 'Idea', 'Weather Update']: category = 'Notification'
    if not timestamp: timestamp = datetime.now() #.strftime("%b %-d %H:%M EDT")
    return {"type" : n_type, "message" : message, "category" : category, "timestamp" : timestamp}


#main function to retrieve dictionaries of messages / categories / notification timestamps
#turn notification timestamps into strings to be displayed as json objects
def getFeedData():

    # ------- notifications based on dynamically retrieved data --------

    #TODO if dailyPeak now at a new high, post new message 
    if not notificationcache.notificationInLastInterval("dailyPeak", timedelta(days=1)):
        notificationcache.addNotification(formatData("dailyPeak", getPeakForDailyData(), category="Notification"))

    #TODO if weather hasn't had notification in past 2 hours, post another one
    if not notificationcache.notificationInLastInterval("weather", timedelta(hours=3)):
        notificationcache.addNotification(formatData("weather", getWeatherNotification(), category="Weather Update"))

    #TODO post average daily
    if not notificationcache.notificationInLastInterval("dailyCompToMonth", timedelta(minutes=30)):
        notificationcache.addNotification(formatData("dailyCompToMonth", getDailyComparisonToPastMonth(), category="Warning"))

    # ------- static data for functionality not yet implemented -------

    if not notificationcache.notificationInLastInterval("water", timedelta(days=3)):
        notificationcache.addNotification(formatData("water", "At your current rate, you're using 12 percent less water than last week.. nice!", category="Congratulations"))

    if not notificationcache.notificationInLastInterval("energy_goal", timedelta(days=7)):
        notificationcache.addNotification(formatData("energy_goal", "Congrats! You reached your energy goal last week -- keep it up!", category="Congratulations"))

    if not notificationcache.notificationInLastInterval("light_on_warning", timedelta(days=4)):
        notificationcache.addNotification(formatData("light_on_warning", "Looks like you left a light on all night yesterday. Make sure you turn off all your lights once you're done using them.", category="Warning"))

    return notificationcache.getNotifications()



# -------------------- message generation logic --------------------

#retrieve a message describing the peak for the day
def getPeakForDailyData():
    data = neurio_api.queryPastDay()
    if not data: return "Your neurio data couldn't be retrieved right now. Make sure to check your wifi connection."
    try:
        peak = max(data, key=lambda sample : sample["consumptionEnergy"])
        #time format: YYYY-MM-DDTHH:MM
        return "Your peak energy consumption today was at {}.".format((datetime.strptime(peak["timestamp"][:16], "%Y-%m-%dT%H:%M") - timedelta(hours=4)).strftime("%-I%p EDT"))
    except:
        return "Your neurio data couldn't be retrieved right now. Make sure to check your wifi connection."


#retrieve a message describing the daily consumption as compared to the monthly consumption
def getDailyComparisonToPastMonth():

    #data retrieval
    try:
        samples_month = [sample['consumptionEnergy'] for sample in neurio_api.queryPastMonth()]
        average_month = sum(samples_month) / len(samples_month)
        samples_today = [sample['consumptionEnergy'] for sample in neurio_api.queryPastDay()]
        average_today = sum(samples_today) / len(samples_today)
    except:
        return None

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
