# import json
# import requests
import subprocess
import yaml

from yaml import Loader, Dumper

# headers = {'Content-Type': 'application/json'}

config_path = "config.yml"
with open(config_path, 'r') as ymlfile:
    conf = yaml.load(ymlfile, Loader=Loader)
playlist_id = conf['player']['playlist_id']
sp = ["spotify_player", "playback"]


def load_playlist():
    subprocess.run(sp + ["start", "context", "--id", playlist_id, "playlist"])
    subprocess.run(sp + ["pause"])


def play():
    subprocess.run(sp + ["play"])


def pause():
    subprocess.run(sp + ["pause"])


def play_pause():
    subprocess.run(sp + ["play-pause"])


def next():
    subprocess.run(sp + ["next"])


def previous():
    subprocess.run(sp + ["previous"])


def volume(lvl):
    subprocess.run(sp + ["volume", str(lvl)])
