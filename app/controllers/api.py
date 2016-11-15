from flask import Blueprint, request, url_for, jsonify

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify(hello='world')

@api.route('/simulation')
def getSimulation():
    return jsonify(status='not implemented')
