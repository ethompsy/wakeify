
import RPi.GPIO as GPIO
import playback
import threading
from time import sleep


class Player(threading.Thread):
    def __init__(self, config):
        self.config = config
        # Get GPIO Pins
        self.v_dn = config['controls']['v_dn']
        self.v_up = config['controls']['v_up']
        self.prv = config['controls']['prev']
        self.pp = config['controls']['pp']
        self.nxt = config['controls']['next']
        # Initialize volume
        self.default_volume = config['alarm']['default_volume']
        self.max_vol = config['alarm']['max_vol']
        self.min_vol = config['alarm']['min_vol']
        self.keep_running = True
        playback.volume(self.default_volume)
        self.volume_now = self.default_volume
        # Setup GPIO
        GPIO.setwarnings(True)
        # Use BCM mode
        GPIO.setmode(GPIO.BCM)
        # define the Encoder switch inputs
        GPIO.setup(self.v_up, GPIO.IN)
        GPIO.setup(self.v_dn, GPIO.IN)
        # define the Button switch inputs
        # GPIO.setup(snz, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.prv, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.nxt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        ### Volume knob events
        # setup callback thread for the A and B encoder
        # use interrupts for all inputs
        self.host = config['player']['host']
        self.uri = config['player']['uri']
        playback.load_playlist()
        GPIO.add_event_detect(
            self.v_dn,
            GPIO.FALLING,
            callback=self.volume_dn,
            bouncetime=4
            )
        GPIO.add_event_detect(
            self.v_up,
            GPIO.FALLING,
            callback=self.volume_up,
            bouncetime=4
            )
        # Button events
        GPIO.add_event_detect(
            self.prv,
            GPIO.FALLING,
            callback=self.pr,
            bouncetime=500
            )
        GPIO.add_event_detect(
            self.pp,
            GPIO.FALLING,
            callback=self.pyps,
            bouncetime=500
            )
        GPIO.add_event_detect(
            self.nxt,
            GPIO.FALLING,
            callback=self.nx,
            bouncetime=500
            )
        threading.Thread.__init__(self)
        self.daemon = False
        self.start()
        return


    def pr(self, b):
        playback.prev()
        return


    def pyps(self, b):
        print "pp pressed"
        playback.pp()
        return


    def nx(self, b):
        playback.next()
        return


    def volume_up(self, k):
        # read both of the switches
        up = GPIO.input(self.v_up)
        down = GPIO.input(self.v_dn)
        print "up: " + str(up)
        print "down: " + str(down)

        if (up == 1) and (down == 0) : # up then down ->
            self.volume_now += 1
            print "direction -> ", self.volume_now
            while (up != 1 and down !=1):
                up = GPIO.input(self.v_up)
                down = GPIO.input(self.v_dn)
            playback.volume(self.volume_now)
            return
        else: # discard all other combinations
            return

    def volume_dn(self, k):
        # read both of the switches
        up = GPIO.input(self.v_up)
        down = GPIO.input(self.v_dn)
        if (up == 0) and (down == 1):
            self.volume_now -= 1
            print "direction <- ", self.volume_now
             # A is already high, wait for A to drop to end the click cycle
            while (up != 1 and down !=1):
                up = GPIO.input(self.v_up)
                down = GPIO.input(self.v_dn)
            playback.volume(self.volume_now)
            return
        else: # discard all other combinations
            return


    def run(self):
        print "Player running!"
        while self.keep_running:
            if playback.tracks() == 0:
                playback.load_playlist()
            sleep(10)
