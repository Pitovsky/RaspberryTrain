import requests
import json
import time
import signal
import sys
from random import randint
import numpy as np

max_speed = 1200
segments_speed = {
    '26': max_speed,
    '24': 550,
    '23': max_speed+200,
    '22': max_speed,
    '34': max_speed+100,
    '35': max_speed,
    '33': max_speed,
    '31': 900,
    '32': 800,
    '21': max_speed,
    '27': max_speed,
    '25': 1000,
    '13': 550,
    '12': max_speed+200,
    '11': 700
}

class TrainController:

    def __init__(self):
        self.speed = 0
        self.slow_timer = 0

    def set_speed(self, des_speed):
        if des_speed != self.speed:
            resp = requests.post('http://192.168.0.180/motor?params=' + str(des_speed))
            if resp.ok:
                self.make_buzz(randint(400,600))
                self.speed = des_speed

    def make_buzz(self, freq=500):
        pass#requests.post('http://192.168.0.180/buzzer?params=' + str(freq))

    def start(self):
        self.set_speed(max_speed)
          
        while True:
            time.sleep(0.15)
            resp = requests.get('http://192.168.0.100:5000/rest/items')
            if resp.ok:
                sections = json.loads(resp.text)['track']['rail_sections']
                cur_segs = []
                cur_segs_speed = []
                for seg, speed in segments_speed.items():
                    if sections[seg]['state'] == 0:
                        cur_segs.append(seg)
                        cur_segs_speed.append(speed)
                print('segs: ' + ','.join(cur_segs))
                if len(cur_segs_speed) > 0:
                    self.set_speed(int(np.mean(cur_segs_speed)))
                #for seg in slow_segments:
                #    if self.slow_timer > 0 or sections[seg]['state'] == 0:
                #        self.set_speed(550)
                #        if self.slow_timer == 0:
                #            self.slow_timer = 10
                #        self.slow_timer -= 1
                #        print('dang seg ' + seg)
                #    else:
                #        self.set_speed(1200)
                #        self.slow_timer = 0
                #        print('ok seg')

if __name__ == '__main__':
    tc = TrainController()
    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        tc.make_buzz()
        tc.set_speed(0)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    tc.start()
