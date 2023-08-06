##!/usr/bin/env python

import itertools
import subprocess
from distutils.spawn import find_executable

class Notifier(object):

    TERMINAL_NOTIFIER = "/usr/local/bin/terminal-notifier"
    OPTIONS = ('message', 'title', 'subtitle', 'group', 'activate', 'open', 'sound', 'execute')

    def __init__(self):
        if not find_executable("terminal-notifier"):
            raise Exception("Meow NEED terminal-notifier")

    def _check_option(self, option):
        if not option in self.OPTIONS:
            raise Exception("options :{}: doesn't exists".format(option))

    def _build_command(self, message, **kwargs):
        command = [self.TERMINAL_NOTIFIER]
        command.extend(["-message", message])
        [ command.extend(["-{}".format(k), v]) for k, v in kwargs.items() ]
        return command

    def _launch_command(self, command):
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def meow(self, message, **kwargs):
        for key in kwargs.keys():
            self._check_option(key)

        command = self._build_command(message, **kwargs)
        self._launch_command(command)

Meow = Notifier()

if __name__ == "__main__":
    print("MEOW")
    noti = Notifier()
    noti.meow("Chapitre 91 OUT", title="One-Punch Man", open="http://readms.net/r/onepunch_man/081/4592/1")
