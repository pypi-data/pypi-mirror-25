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
import json
import subprocess
import signal

from nxtools.common import decode_if_py3
from nxtools.misc import indent
from nxtools.logging import *

__all__ = ["ffprobe"]

def ffprobe(input_path, verbose=False):
    """Runs ffprobe on file and returns python dict with result"""
    if not os.path.exists(input_path):
        logging.error("ffprobe: file does not exist ({})".format(input_path))
        return False
    cmd = [
            "ffprobe",
            "-show_format",
            "-show_streams",
            "-print_format", "json",
            input_path
        ]
    FNULL = open(os.devnull, "w")
    logging.debug("Executing {}".format(" ".join(cmd)))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = ""
    while True:
        ch = decode_if_py3(proc.stdout.read(1))
        if not ch:
            break
        res += ch
    res += decode_if_py3(proc.stdout.read())
    if proc.returncode:
        if verbose:
            logging.error("Unable to read media file\n\n{}\n\n".format(indent(proc.stderr.read())))
        else:
            logging.warning("Unable to read media file {}".format(input_path))
        return False
    return json.loads(res)
