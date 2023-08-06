#! python3
# countdown.py - A simple countdown script

import os
import time
from alarm import Alarm

current_directory = os.getcwd()


class Countdown(object):

    def __init__(self, start_time, alarm=False, **kwargs):

        self.start_time = start_time

        self.alarm = None

        if alarm:

            sound = kwargs.get('sound', None)

            duration = kwargs.get('duration', None)

            self.alarm = Alarm(sound, duration)

    def start(self):

        time_left = self.start_time

        while time_left > 0:

            print(time_left)

            time.sleep(1)

            time_left = time_left - 1

        if self.alarm:

            self.alarm.start()
