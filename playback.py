import json
import requests
import yaml


headers = {'Content-Type': 'application/json'}

config_path = "config.yml"
with open(config_path, 'r') as ymlfile:
    conf = yaml.load(ymlfile)
host = conf['player']['host']
uri = conf['player']['uri']
url = "http://" + host + ":6680/mopidy/rpc"


def load_playlist():
    payload = """{
        "method": "core.tracklist.clear",
        "jsonrpc":  "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)
    payload = """{
        "method": "core.tracklist.add",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {
        "tracks": null,
        "at_position": null,
        "uri": "%s"
        }
        }""" % uri
    r = requests.post(url, headers=headers, data=payload)


def tracks():
    payload = """{
        "method": "core.tracklist.get_length",
        "jsonrpc":  "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)
    return json.loads(r.text)['result']


def play():
    payload = """{
        "method": "core.playback.play",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)


def stop():
    payload = """{
        "method": "core.playback.stop",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)


def pause():
    payload = """{
        "method": "core.playback.pause",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)


def resume():
    payload = """{
        "method": "core.playback.resume",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)


def next():
    payload = """{
        "method": "core.playback.next",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    print "next"
    r = requests.post(url, headers=headers, data=payload)   


def prev():
    payload = """{
        "method": "core.playback.previous",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    print "previous"
    r = requests.post(url, headers=headers, data=payload)   


def state():
    payload = """{
        "method": "core.playback.get_state",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)
    # print json.loads(r.text)['result']
    return json.loads(r.text)['result']


def pp():
    st = state()
    # print st
    if st == 'paused':
        # print "resume"
        resume()
    elif st == 'stopped':
        # print "play"
        play()
    elif st == 'playing':
        # print "pause"
        pause()


def volume(lvl):
    payload = """{
        "method": "core.playback.set_volume",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {"volume": """ + str(lvl) + """}
    }"""
    r = requests.post(url, headers=headers, data=payload)


def check_volume():
    payload = """{
        "method": "core.playback.get_volume",
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    }"""
    r = requests.post(url, headers=headers, data=payload)
    return json.loads(r.text)['result']
