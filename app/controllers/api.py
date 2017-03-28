from flask import Blueprint, request, url_for, jsonify
from datetime import datetime

from app.models import Simulation, Room, SmartSocket, PowerConsumption, db
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

@api.route('/rooms', methods=['POST'])
def addRoom():
    body = request.get_json()
    name = body['name']
    new_room = Room(name=name)
    db.session.add(new_room)
    db.session.commit()
    return jsonify(success=new_room.serialize())

@api.route('/rooms', methods=['GET'])
def getRooms():
    rooms = [r.serialize() for r in Room.query.all()]
    return jsonify(rooms=rooms)

@api.route('/rooms/<int:roomId>/sockets', methods=['GET'])
def getSocketsByRoom(roomId):
    return jsonify(sockets=Room.getSockets(roomId), roomId=roomId)

@api.route('/sockets', methods=['POST'])
def addSocket():
    body = request.get_json()
    name = body['name']
    roomId = body['roomId']
    new_socket = SmartSocket(name=name, roomId=roomId)
    db.session.add(new_socket)
    db.session.commit()
    return jsonify(success=new_socket.serialize())

@api.route('/sockets', methods=['GET'])
def getSockets():
    sockets = [s.serialize() for s in SmartSocket.query.all()]
    return jsonify(sockets=sockets)

@api.route('/sockets/<int:socketId>/logs', methods=['POST'])
def logPower(socketId):
    timestamp = datetime.now()
    power = request.get_json()['power']
    log_entry = PowerConsumption(timestamp=timestamp, socketId=socketId, power=power)
    db.session.add(log_entry)
    db.session.commit()
    return jsonify(success=log_entry.serialize())

@api.route('/sockets/<int:socketId>/logs', methods=['GET'])
def getPowerLogsBySocket(socketId):
    return jsonify(logs=SmartSocket.getPowerLogs(socketId), socketId=socketId)

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
