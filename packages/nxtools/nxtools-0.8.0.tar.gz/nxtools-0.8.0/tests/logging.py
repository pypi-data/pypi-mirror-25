#!/usr/bin/env python

import _bootstrap
from nxtools import *

print

logging.debug("Hello world")
logging.info("Hello world")
logging.warning("Hello world")
logging.error("Hello world")
logging.goodnews("Hello world")

print

logging.user = "Nebula"

logging.debug("Hello world")
logging.info("Hello world")
logging.warning("Hello world")
logging.error("Hello world")
logging.goodnews("Hello world")

print

try:
    a = 1/0
except Exception:
    log_traceback()
