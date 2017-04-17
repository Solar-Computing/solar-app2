from __future__ import division
from datetime import datetime, timedelta
import app.neurioclient.my_keys as my_keys
import neurio
import pprint
import time
import sys


# Setup authentication & create client that can authenticate itself -------------------------------
tp = neurio.TokenProvider(key=my_keys.key, secret=my_keys.secret)
nc = neurio.Client(token_provider=tp)

# Retrieve sensor ID and location ID --------------------------------------------------------------
sensor_id = nc.get_user_information()["locations"][0]["sensors"][0]["sensorId"]
location_id = nc.get_user_information()["locations"][0]["id"]



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
    try:
        timeinterval = specifyTimeInterval("hours", 1)
        end = (datetime.utcnow()).replace(microsecond=0).isoformat()
        data = nc.get_samples(sensor_id=sensor_id, start=timeinterval, end=end,
          granularity="hours", frequency=1)
        return data
    except:
        return []


"""
  this function will return:
  - list of up to 24 data points for each hour of data collected in the past 24 hours
  - an empty list if the neurio collected no data in the past day
"""
def queryPastDay():
    try:
        timeinterval = specifyTimeInterval("hours", 24)
        end = (datetime.utcnow()).replace(microsecond=0).isoformat()
        data = nc.get_samples(sensor_id=sensor_id, start=timeinterval, end=end,
            granularity="hours", frequency=1, per_page=500)
        return data
    except:
        return []

"""
  this function will return:
  - list of the data points for each hour of data collected in the past 30 days
  - an empty list if the neurio collected no data in the past month
"""
def queryPastMonth():
    try:
        timeinterval = specifyTimeInterval("hours", 720)
        end = (datetime.utcnow()).replace(microsecond=0).isoformat()
        data = nc.get_samples(sensor_id=sensor_id, start=timeinterval, end=end,
            granularity="hours", frequency=2, per_page=500)
        return data
    except:
        return []


"""
  inputs: 
  - start in the format returned by javascript's toUTCString() function
  - end in the format returned by javascript's toUTCString() function

  this function will return:
  - list of the data points for each hour of data collected in the specified interval
"""
def queryInterval(start, end, aggregate):
    #parse aggregate
    aggregator = "hours"
    if aggregate == "daily": aggregator = "days"
    elif aggregate == "monthly": aggregator = "months"

    #retrieve data
    try:
        start = datetime.strptime(start, "%a, %d %b %Y %X GMT").isoformat()
        end = datetime.strptime(end, "%a, %d %b %Y %X GMT").isoformat()
        data = nc.get_samples(sensor_id=sensor_id, start=start, end=end,
            granularity=aggregator, frequency=1, per_page=500)
        return data
    except:
        return []


'''
  return the average for a set of samples
'''
def findIntervalAverage(samples):
    data = [int(sample["consumptionPower"]) for sample in samples]
    return {"ACPrimaryLoad":sum(data)/len(data), "PVPowerOutput":0}


'''
  change format of the samples to how the front end parses the data
  currently no PV power output, so that value is changed to zero -- should be changed dynamically once there is information
'''
def convertSamplesToSimulationFormat(samples):
    newsamples = [{"ACPrimaryLoad":sample["consumptionPower"], "PVPowerOutput": 0, "timestamp":datetime.strptime(sample["timestamp"], "%Y-%m-%dT%X.000Z").strftime("%a, %d %b %Y %X GMT")} for sample in samples]
    return newsamples







