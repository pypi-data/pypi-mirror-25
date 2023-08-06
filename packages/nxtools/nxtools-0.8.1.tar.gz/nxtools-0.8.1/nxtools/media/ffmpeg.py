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

from __future__ import print_function

import os
import re
import time
import subprocess
import copy
import signal

from nxtools.common import decode_if_py3
from nxtools.misc import indent
from nxtools.shell import Shell
from nxtools.logging import *

__all__ = ["enable_ffmpeg_debug", "FFMPEG", "ffmpeg"]

FFMPEG_DEBUG = False
def enable_ffmpeg_debug():
    global FFMPEG_DEBUG
    FFMPEG_DEBUG = True

class FFMPEG():
    def __init__(
            self,
            input_path,
            output_path,
            output_format=[],
            input_format=[]
            ):
        if FFMPEG_DEBUG:
            logging.warning("FFMPEG debug mode is enabled")
        self.proc = None
        self.cmd = ["ffmpeg", "-y"]
        for p in input_format:
            self.cmd.extend(self.make_profile(p))
        self.cmd.extend(["-i", input_path])
        for p in output_format:
            self.cmd.extend(self.make_profile(p))
        self.cmd.append(output_path)
        self.reset_stderr()

    def reset_stderr(self):
        self.buff = self.error_log = ""

    @staticmethod
    def make_profile(p):
        cmd = []
        if type(p) == list and len(p) == 2:
            key, val = p
        elif type(p) == list:
            key = p[0]
            val = False
        else:
            key = p
            val = False
        cmd.append("-" + str(key))
        if val:
            cmd.append(str(val))
        return cmd

    @property
    def is_running(self):
        return bool(self.proc) and self.proc.poll() == None

    @property
    def stdin(self):
        return self.proc.stdin

    @property
    def stdout(self):
        return self.proc.stdout

    @property
    def stderr(self):
        return self.proc.stderr

    @property
    def return_code(self):
        return self.proc.returncode

    def start(self, stdin=None, stdout=None, stderr=subprocess.PIPE):
        self.reset_stderr()
        logging.debug("Executing", " ".join(self.cmd))
        self.proc = subprocess.Popen(
                self.cmd,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
            )

    def stop(self):
        if not self.proc:
            return False
        self.proc.send_signal(signal.SIGINT)
        self.proc.wait()
        return True

    def wait(self, progress_handler=None):
        while True:
            if not self.process(progress_handler=progress_handler):
                break
        self.error_log += decode_if_py3(self.stderr.read())

    def process(self, progress_handler=None):
        ch = decode_if_py3(self.proc.stderr.read(1))
        if not ch:
            return False
        if ch in ["\n", "\r"]:
            if self.buff.startswith("frame="):
                m = re.match(r".*frame=\s*(\d+)\s*fps.*", self.buff)
                if m and progress_handler:
                    progress_handler(int(m.group(1)))
            else:
                self.error_log += self.buff + "\n"
            if FFMPEG_DEBUG:
                print (self.buff.rstrip())
            self.buff = ""
        else:
            self.buff += ch
        return True



def ffmpeg(input_path, output_path, output_format=[], input_format=[], **kwargs):
    """Universal ffmpeg wrapper with progress and error handling.

    Parameters
    ----------
    input_path : string
        input file path
    output_path : string
        output file path
    output_format : list
        list of (param, value) tuples specifiing output format
    start : float
        start time in seconds (using fast seek)
    duration : float
        duration in seconds
    input_format : list
        input format specification. same syntax as profile
    progress_handler : function
        method which will receive current progress as float
    stdin : file
        standard input (usable when input_path=="-")
    stdout : file
        standard output (usable when output_path=="-)"
    """

    input_format = copy.copy(input_format)
    output_format = copy.copy(output_format)

    if kwargs.get("start", False):
        input_format.append(["ss", kwargs["start"]])
    if kwargs.get("duration", False):
        output_format.append(["t", kwargs["duration"]])


    ff = FFMPEG(
            input_path,
            output_path,
            output_format=output_format,
            input_format=input_format
            )

    ff.start(
            stdin=kwargs.get("stdin", None),
            stdout=kwargs.get("stdout", None),
            stderr=kwargs.get("stderr", subprocess.PIPE)
        )
    if not ff.wait(kwargs.get("progress_handler", None)):
        return False # keyboard interrupt

    if ff.return_code:
        logging.error(
            "Problem occured during transcoding\n\n{}\n\n".format(indent(ff.error_log))
            )
        return False
    return True

