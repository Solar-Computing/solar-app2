from flask import Blueprint, request, url_for, jsonify
from app.models import Simulation
from app.neurioclient import neurio_api
api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(hello='world')

@api.route('/neurioHourly')
def getNeurioHourly():
    return jsonify(neurio_api.queryPastHour())

@api.route('/neurioDaily')
def getNeurioDaily():
    return jsonify(neurio_api.queryPastDay())

@api.route('/neurioMonthly')
def getNeurioMonthly():
    return jsonify(neurio_api.queryPastMonth())

@api.route('/simulations', methods=['POST'])
def getSimulation():
    body = request.get_json()
    start = body['start']
    end = body['end']
    aggregate = body['aggregate']
    results = Simulation.getRange(start, end, aggregate)
    average = Simulation.getAverage(start, end)
    return jsonify(contents=results, average=average)

@api.route('/dailyLoad')
def getDaily():
    return jsonify(status='sup')

@api.route('/weeklyLoad')
def getWeekly():
    return jsonify(load='week')

@api.route('/test')
def test():
    return jsonify(
        [
            {"name": "General", "toggle": {"switchIsOn": False}, "options": [
                {"name": "Temperature", "optionType": "slider", "state": {"minimum": "20", "maximum":"120"}},
                {"name": "Microwave", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Dishwasher", "optionType": "switch", "state": {"switchIsOn": False}}
                ]
            },
            {"name": "Kitchen", "toggle": {"switchIsOn": False}, "options": [
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Microwave", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Dishwasher", "optionType": "switch", "state": {"switchIsOn": False}}
                ]
            },
            {"name": "Living Room", "toggle": {"switchIsOn": False}, "options": [
                {"name": "Light 1", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Light 2", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Outlet 1", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Outlet 2", "optionType": "switch", "state": {"switchIsOn": False}}
                ]
            },
            {"name": "Bed Room", "toggle": {"switchIsOn": False}, "options": [
                {"name": "Outlet 1", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Outlet 2", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Heater", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}},
                {"name": "Lights", "optionType": "switch", "state": {"switchIsOn": False}}
                ]
            }
        ])
