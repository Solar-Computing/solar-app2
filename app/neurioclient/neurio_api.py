import neurio
import sys
import pprint
from datetime import datetime, timedelta
import my_keys
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
  string of datetime timestamp to be parsed by the api call
"""
def specifyTimeInterval(unit, number):
    interval = None
    if unit == "hours":
        return (datetime.utcnow()-timedelta(hours=number)+timedelta(minutes=2)).replace(microsecond=0).isoformat()
    elif unit == "minutes":
        return (datetime.utcnow()-timedelta(minutes=number)).replace(microsecond=0).isoformat()
    elif unit == "seconds":
        (datetime.utcnow()-timedelta(seconds=number)).replace(microsecond=0).isoformat()
    else:
        raise ValueError('Invalid unit specified for time interval query')


# Functions to retrieve data from the neurio sensor ------------------------------------------------

"""
  this function will return:
  - one data point for data collected in the past hour
  - an empty list if the neurio collected no data in the past hour
"""
def queryPastHour():
    timeinterval = specifyTimeInterval("hours", 1)
    end = (datetime.utcnow()).replace(microsecond=0).isoformat()
    data = nc.get_samples(sensor_id=sensor_id, start=timeinterval, end=end,
        granularity="hours", frequency=1)
    return data


"""
  this function will return:
  - list of up to 24 data points for each hour of data collected in the past 24 hours
  - an empty list if the neurio collected no data in the past day
"""
def queryPastDay():
    timeinterval = specifyTimeInterval("hours", 24)
    end = (datetime.utcnow()).replace(microsecond=0).isoformat()
    data = nc.get_samples(sensor_id=sensor_id, start=timeinterval, end=end,
        granularity="hours", frequency=1)
    return data


"""
  this function will return:
  - list of the data points for each hour of data collected in the past 30 days
  - an empty list if the neurio collected no data in the past month
"""
def queryPastMonth():
    timeinterval = specifyTimeInterval("hours", 720)
    end = (datetime.utcnow()).replace(microsecond=0).isoformat()
    data = nc.get_samples(sensor_id=sensor_id, start=timeinterval, end=end,
        granularity="hours", frequency=1)
    return data


