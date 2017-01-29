from flask import Blueprint, request, url_for, jsonify
from app.models import Simulation
api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(hello='world')

@api.route('/simulations', methods=['POST'])
def getSimulation():
    body = request.get_json()
    start = body['start']
    end = body['end']
    results = db.session.execute(Simulation.getRange(start, end)).fetchall()
    return jsonify(contents=results, average="not implemented")

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
