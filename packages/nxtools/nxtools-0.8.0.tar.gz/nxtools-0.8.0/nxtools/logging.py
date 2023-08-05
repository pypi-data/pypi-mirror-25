# The MIT License (MIT)
#
# Copyright (c) 2015 - 2017 imm studios, z.s.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import sys
import traceback

from .common import PLATFORM
from .misc import indent

__all__ = ["logging", "log_traceback", "critical_error"]


DEBUG, INFO, WARNING, ERROR, GOOD_NEWS = range(5)

class Logging():
    def __init__(self, user=""):
        self.user = user
        self.handlers = []
        self.formats = {
            INFO      : "INFO       {0} {1}",
            DEBUG     : "\033[34mDEBUG      {0} {1}\033[0m",
            WARNING   : "\033[33mWARNING\033[0m    {0} {1}",
            ERROR     : "\033[31mERROR\033[0m      {0} {1}",
            GOOD_NEWS : "\033[32mGOOD NEWS\033[0m  {0} {1}"
            }

        self.formats_win = {
            DEBUG     : "DEBUG     {0} {1}",
            INFO      : "INFO      {0} {1}",
            WARNING   : "WARNING   {0} {1}",
            ERROR     : "ERROR     {0} {1}",
            GOOD_NEWS : "GOOD NEWS {0} {1}"
            }

    def add_handler(self, handler):
        if not handler in self.handlers:
            self.handlers.append(handler)

    def _send(self, msgtype, *args, **kwargs):
        message = " ".join([str(arg) for arg in args])
        user = kwargs.get("user", self.user)
        if user:
            user = " {:<15}".format(user)
        if kwargs.get("handlers", True):
            for handler in self.handlers:
                handler(user=self.user, message_type=msgtype, message=message)
        if PLATFORM == "unix":
            try:
                print(self.formats[msgtype].format(user, message))
            except Exception:
                print(message.encode("utf-8"))
        else:
            try:
                print(self.formats_win[msgtype].format(user, message))
            except Exception:
                print(message.encode("utf-8"))

    def debug(self, *args, **kwargs):
        """Log debug message"""
        self._send(DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        """Log info message"""
        self._send(INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        """Log warning message"""
        self._send(WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        """Log error message"""
        self._send(ERROR, *args, **kwargs)

    def goodnews(self, *args, **kwargs):
        """Log good news"""
        self._send(GOOD_NEWS, *args, **kwargs)

logging = Logging()


def log_traceback(message="Exception!", **kwargs):
    tb = traceback.format_exc()
    msg = "{}\n\n{}".format(message, indent(tb))
    logging.error(msg, **kwargs)
    return msg

def critical_error(msg, **kwargs):
    logging.error(msg, **kwargs)
    logging.debug("Critical error. Terminating program.")
    sys.exit(1)
