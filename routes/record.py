from inc import *
from flask import current_app

class HostState:
    def __init__(self, hostTime, paused, playing, speed):
        self.hostTime = hostTime
        self.paused = paused
        self.playing = playing
        self.speed = speed
    
def record():
    response = request.get_json()
    print(response)
    current_app.config[response["token"]] = HostState(response["hostTime"], response["paused"], response["playing"], response["speed"])
    return Response(status=200)
    