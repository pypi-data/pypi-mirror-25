import os
import tempfile
import re
import configparser
import sys
import logging
from instadb.connection import Connection

logger = logging.getLogger(__name__)

connect = False
vars()["connections"] = []
for key in os.environ:
  match = re.match('(.*)_DATABASE_URL', key)
  if match:
    vars()[match.group(1)] = Connection(os.environ.get(match.group()), connect=connect)
    vars()["connections"].append(match.group(1))
