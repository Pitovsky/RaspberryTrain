import requests
import json
import time
import signal
import sys
import threading
from random import randint
import numpy as np

from traincam import TrainCam

max_speed = 1400
segments_speed = {
    '26': max_speed,
    '24': 750,
    '23': max_speed,
    '22': max_speed,
    '34': max_speed,
    '35': max_speed,
    '33': max_speed,
    '31': 900,
    '32': 750,
    '21': max_speed,
    '27': max_speed,
    '25': max_speed,
    '13': 750,
    '12': max_speed,
    '11': 900,
}

train_base_url = 'http://127.0.0.1:5000' #'http://192.168.0.180'
stats_base_url = 'http://127.0.0.1:5000' #'http://192.168.0.100:5000'

class TrainController:

    def __init__(self, tick_time=0.15):
        self.tick_time = tick_time
        self.speed = 0
        self.stop_timer = 0
        self.cur_segs = {}
        self.cam = TrainCam()
        self.running = True
        self.job = threading.Thread(target=self.control)

    def set_speed(self, des_speed):
        if des_speed != self.speed:
            resp = requests.post(train_base_url + '/motor?params=' + str(des_speed))
            if resp.ok:
                self.speed = des_speed

    def make_buzz(self, freq=500):
        pass#requests.post(train_base_url + '/buzzer?params=' + str(freq))
    
    def control(self):
        while self.running:
            time.sleep(self.tick_time)
            
            if self.cam.is_dangerous():
                print('cam sees something dangerous, stopping')
                self.make_buzz()
                # if 26 in self.cur_segs: TODO switch the rail
                self.stop_timer = int(1.0 / self.tick_time)
            if self.stop_timer > 0:
                 self.stop_timer -= 1
                 self.set_speed(0)
            else:
                resp = requests.get(stats_base_url + '/rest/items')
                if resp.ok:
                    sections = json.loads(resp.text)['track']['rail_sections']
                    cur_segs = {}
                    for seg, speed in segments_speed.items():
                        if sections[seg]['state'] == 0:
                            cur_segs[seg] = speed
                    print('segs: ' + ','.join(cur_segs))
                    if len(cur_segs) > 0:
                        self.set_speed(int(np.mean([s for s in cur_segs.values()])))
    
    def start(self):
        self.set_speed(max_speed)
        self.cam.start()
        self.job.start()
    
    def start_and_wait(self):
        self.start()
        time.sleep(0.5)
        self.job.join()
    
    def stop(self):
        self.running = False
        self.cam.stop()
        self.job.join()
        self.set_speed(0)
        self.make_buzz()

if __name__ == '__main__':
    tc = TrainController()
    def signal_handler(sig, frame):
        print('SIGTERM recieved, stopping controller')
        tc.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    tc.start_and_wait()
