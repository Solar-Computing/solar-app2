from flask import Blueprint, request, url_for, jsonify
from datetime import datetime

from app.models import Simulation, Home, Circuit, PowerConsumption, db
from app.neurioclient import neurio_api
from app.controllers import feedgenerator
api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(hello='world')

@api.route('/feedData')
def feedPopulationData():
    return jsonify(feedgenerator.getFeedData())

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

@api.route('/homes', methods=['POST'])
def addHome():
    body = request.get_json()
    name = body['name']
    new_home = Home(name=name)
    db.session.add(new_home)
    db.session.commit()
    return jsonify(success=new_home.serialize())

@api.route('/homes', methods=['GET'])
def getHomes():
    homes = [r.serialize() for r in Home.query.all()]
    return jsonify(homes=homes)

@api.route('/homes/<int:homeId>/circuits', methods=['GET'])
def getCircuitsByHome(homeId):
    return jsonify(circuits=Home.getCircuits(homeId), homeId=homeId)

@api.route('/circuits', methods=['POST'])
def addCircuit():
    body = request.get_json()
    name = body['name']
    homeId = body['homeId']
    new_circuit = Circuit(name=name, homeId=homeId)
    db.session.add(new_circuit)
    db.session.commit()
    return jsonify(success=new_circuit.serialize())

@api.route('/circuits', methods=['GET'])
def getCircuits():
    circuits = [s.serialize() for s in Circuit.query.all()]
    return jsonify(circuits=circuits)

@api.route('/circuits/<int:circuitId>/logs', methods=['POST'])
def logPower(circuitId):
    timestamp = datetime.now()
    power = request.get_json()['power']
    log_entry = PowerConsumption(timestamp=timestamp, circuitId=circuitId, power=power)
    db.session.add(log_entry)
    db.session.commit()
    return jsonify(success=log_entry.serialize())

@api.route('/circuits/<int:circuitId>/logs', methods=['GET'])
def getPowerLogsByCircuit(circuitId):
    return jsonify(logs=Circuit.getPowerLogs(circuitId), circuitId=circuitId)

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
