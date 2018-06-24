import RPi.GPIO as GPIO
import datetime
import os
import playback
import threading
import time
from time import sleep
import yaml


class Alarm(threading.Thread):
    def __init__(self, config):
        self.config = config
        self.alarm_day = False
        self.snoozed = False
        self.snooze_time = 60 * 5
        self.wake_hour = 0
        self.wake_min = 0
        self.wakeup_period = 60 * 60
        self.alarm = False
        self.keep_running = True
        self.uri = ""
        self.host = ""
        snz = config['controls']['snooze']
        # Setup GPIO
        GPIO.setwarnings(True)
        # Use BCM mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(
            snz,
            GPIO.IN,
            pull_up_down=GPIO.PUD_UP
            )
        GPIO.add_event_detect(
            snz,
            GPIO.FALLING,
            callback=self.snooze,
            bouncetime=200
            )
        threading.Thread.__init__(self)
        self.daemon = False
        self.start()
        return


    def run(self):
        print "Alarm running!"
        while self.keep_running:
            self.load_schedule()
            if self.alarm_day:
                now = time.localtime()
                if (self.wake_hour == str(time.localtime().tm_hour)):
                    now_min = time.localtime().tm_min
                    if now_min < 10:
                        now_min = '0' + str(now_min)
                    else:
                        now_min = str(now_min)
                    if (self.wake_min == now_min):
                        self.alarm_time()
            time.sleep(10)
        return


    def snooze(self, b):
        if self.alarm:
            print "Snoozed!!"
            self.snoozed = True
            playback.pause()
        return


    def alarm_time(self):
        print "ALARM TIME!!!"
        self.alarm = True
        playback.load_playlist()
        time.sleep(2)
        playback.play()
        while self.wakeup_period:
            st = playback.state()
            if (st == 'paused' or st == 'stopped'):
                self.snoozed = True
            while self.snoozed:
                snooze_time = self.snooze_time
                while snooze_time:
                    time.sleep(1)
                    snooze_time -= 1
                    self.wakeup_period -= 1
                self.snoozed = False
                playback.play()
            time.sleep(1)
            self.wakeup_period -= 1
            if self.wakeup_period < 0:
                self.wakeup_period = 0
        return


    def load_schedule(self):
        day_num = time.localtime().tm_wday
        day = {
            0: 'mon',
            1: 'tue',
            2: 'wed',
            3: 'thu',
            4: 'fri',
            5: 'sat',
            6: 'sun',
            }.get(day_num, None)
        wakeup = self.config['alarm']['schedule'][day]
        self.snooze_time = self.config['alarm']['snooze_time']
        self.wakeup_period = self.config['alarm']['wakeup_period']
        try:
            wakeup = wakeup.split(':')
            self.wake_hour = wakeup[0]
            self.wake_min = wakeup[1]
            self.alarm_day = True
        except:
            self.alarm_day = False


    def die(self):
        self.keep_running = False

