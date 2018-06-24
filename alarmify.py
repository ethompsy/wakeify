from daemonize import Daemonize
from time import sleep
import player
import wakeup
import yaml


def config(config_path):
    with open(config_path, 'r') as ymlfile:
        return yaml.load(ymlfile)


def main():
    config_path = "./config.yml"
    conf = config(config_path)
    wakeup.Alarm(conf)
    player.Player(conf)
    while True:
        sleep(5)
    return


if __name__ == "__main__": main()
#pid = "/tmp/alarmify.pid"
#daemon = Daemonize(app="alarmify", pid=pid, action=main)
#daemon.start()
