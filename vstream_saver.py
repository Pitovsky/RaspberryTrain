import cv2
import signal
import sys

cap = cv2.VideoCapture('http://192.168.0.190:8080/stream/video.mjpeg')
#cap.set(3,320)
#cap.set(4,240)
print(cap.isOpened())

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('videos/test9.mp4', fourcc, 25.0, (320,240))

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    cap.release()
    out.release()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while(True):
    ret, frame = cap.read()
    out.write(frame)


