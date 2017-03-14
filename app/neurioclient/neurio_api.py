import neurio
import sys
import pprint
from datetime import datetime, timedelta
import app.neurioclient.my_keys as my_keys
import time


# Setup authentication & create client that can authenticate itself -------------------------------
try:
  tp = neurio.TokenProvider(key=my_keys.key, secret=my_keys.secret)
  nc = neurio.Client(token_provider=tp)

  # Retrieve sensor ID and location ID --------------------------------------------------------------
  sensor_id = nc.get_user_information()["locations"][0]["sensors"][0]["sensorId"]
  location_id = nc.get_user_information()["locations"][0]["id"]

except:
  print("error authenticating with server")


# Functions for specifying the time interval -------------------------------------------------------

"""
args
  string unit: the unit of the time you want to specify for the time interval
  int number: the value of the time associated with the unit

returns
  datetime time interval to be parsed by the api call
  int frequency associted with retrieving a single data point for the time interval

"""
def specifyTimeInterval(unit, number):
    interval = None
    frequency = None
    if unit == "hours":
        interval = getHourInterval(number)
        frequency = number * 60
        frequency -= frequency % 5
    elif unit == "minutes":
        interval = getMinuteInterval(number)
        frequency = number - number%5
    elif unit == "seconds":
        interval = getSecondInterval(number)
        frequency = number - number%5
    else:
        raise ValueError('Invalid unit')
    return interval, frequency


def getMinuteInterval(minutes):
    return (datetime.utcnow()-timedelta(minutes=minutes)).replace(microsecond=0).isoformat()

def getHourInterval(hours):
    return (datetime.utcnow()-timedelta(hours=hours)).replace(microsecond=0).isoformat()

def getSecondInterval(seconds):
    return (datetime.utcnow()-timedelta(seconds=seconds)).replace(microsecond=0).isoformat()


# Functions to retrieve data from the neurio sensor ------------------------------------------------

"""
  this function will return:
  - one data point for data collected in the past hour
  - an empty list if the neurio collected no data in the past hour
"""
def queryPastHour():
    timeinterval, frequency = specifyTimeInterval("hours", 1)
    data = nc.get_samples(sensor_id=sensor_id, start=timeinterval,
        granularity="hours", frequency=1)
    return data


"""
  this function will return:
  - list of up to 24 data points for each hour of data collected in the past 24 hours
  - an empty list if the neurio collected no data in the past day
"""
def queryPastDay():
    timeinterval, frequency = specifyTimeInterval("hours", 24)
    data = nc.get_samples(sensor_id=sensor_id, start=timeinterval,
        granularity="hours", frequency=1)
    return data


"""
  this function will return:
  - list of the data points for each hour of data collected in the past 30 days
  - an empty list if the neurio collected no data in the past month
"""
def queryPastMonth():
    timeinterval, frequency = specifyTimeInterval("hours", 720)
    data = nc.get_samples(sensor_id=sensor_id, start=timeinterval,
        granularity="hours", frequency=1)
    return data


