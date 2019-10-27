from flask import Flask, render_template, request, jsonify
from random import random

import json

sections = ['26', '24', '23', '22', '34', '35', '33', '31', '32', '21', '27', '25', '13', '12', '11']
current_section = 0
app = Flask(__name__)

@app.route('/rest/items', methods=['GET'])
def get_stats():
    global current_section
    if random() > 0.7:
        current_section = (current_section + 1) % (len(sections) + 1) # +1 for invalid section
    data = {}
    for section in sections:
        if current_section < len(sections) and section == sections[current_section]:
            data[section] = {'state': 0}
        else:
            data[section] = {'state': 1}
    print('sending track info')
    return jsonify({'track': {'rail_sections': data}})

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
