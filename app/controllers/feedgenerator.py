from app.neurioclient import neurio_api
from flask import jsonify
from datetime import datetime


''' 
  logo categories:
    'logo'
    'goal'
    'trophy'
    'target'
    'light-bulb'
    'announcement'
'''

#main function to retrieve dictionaries of messages / logos / notification timestamps
def getFeedData():
    feedlist = []
    if getPeakForDailyData(): feedlist.append({"message" : getPeakForDailyData(), "logo" : 'light-bulb.png', "timestamp" : datetime.now().strftime("%b %-d %-I%p ET")})
    if getDailyComparisonToPastMonth(): feedlist.append({"message" : getWeatherNotification, "logo" : "target.png", "timestamp" : datetime.now().strftime("%b %-d %-I%p ET")})
    if getWeatherNotification(): feedlist.append({"message" : getWeatherNotification, "logo" : "sun.png", "timestamp" : datetime.now().strftime("%b %-d %-I%p ET")})
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
    return "It will be very sunny today, so make sure to close your blinds to block out heat!"
