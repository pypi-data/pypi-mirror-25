#! python3
# countdown.py - A simple alarm script

import os
import subprocess
import time


class Alarm(object):

    process = None

    def __init__(self, sound=None, duration=None):

        self.sound = sound

        self.duration = 5

        if duration is not None:

            self.duration = duration

    def start(self):

        if self.sound is None:

            self.sound = os.getcwd() + '/assets/alarm.wav'

        self.process = subprocess.Popen(['aplay', self.sound])

        time.sleep(self.duration)

        self.stop()

    def stop(self):

        self.process.kill()
