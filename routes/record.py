from inc import *
from flask import current_app

class HostState:
    def __init__(self, hostTime, paused, playing, speed):
        self.hostTime = hostTime
        self.paused = paused
        self.playing = playing
        self.speed = speed