from flask import Flask, render_template, request, jsonify

import json


app = Flask(__name__)

@app.route('/rest/items', methods=['GET'])
def get_stats():
    print('sending track info')
    return jsonify({'track': {'rail_sections': {
        '26': {'state': 1},
        '24': {'state': 1},
        '23': {'state': 1},
        '22': {'state': 0},
        '34': {'state': 1},
        '35': {'state': 1},
        '33': {'state': 1},
        '31': {'state': 1},
        '32': {'state': 1},
        '21': {'state': 1},
        '27': {'state': 1},
        '25': {'state': 1},
        '13': {'state': 1},
        '12': {'state': 1},
        '11': {'state': 1}}}})

@app.route('/motor', methods=['POST', 'GET'])
def set_motor_speed():
    speed = request.args.get('params')
    print('setting speed to ' + str(speed))
    return 'OK'

@app.route('/buzzer', methods=['POST', 'GET'])
def make_buzz():
    speed = request.args.get('params')
    print('buzzing at ' + str(speed))
    return 'OK'

if __name__ == '__main__':
    app.run()
