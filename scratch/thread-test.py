import time
import os
import threading

class Alarm(threading.Thread):
    def __init__(self):
        super(Alarm, self).__init__()
        # self.hours = int(hours)
        # self.minutes = int(minutes)
        self.keep_running = True

    def run(self):
        while self.keep_running:
            now = time.localtime()
            hour = str(now.tm_hour)
            minute = str(now.tm_min)
            second = str(now.tm_sec)
            timestring = hour + ':' + minute + ':' + second
            print(timestring)
            time.sleep(1)
            # if (now.tm_hour == self.hours and now.tm_min == self.minutes):
            #     print("ALARM NOW!")
            #     os.popen("test.mp3")
            #     return
        # time.sleep(60)
    def just_die(self):
        self.keep_running = False

alarm = Alarm()
alarm.run()

while True:
    text = str(raw_input())
    if text == "stop":
        alarm.just_die()
        break
