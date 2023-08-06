import os, sys, re
from instadb.connection import Connection

autoconnect = os.environ.get("INSTADB_AUTOCONNECT", False)
vars()["connections"] = []
for key in os.environ:
  match = re.match('(.*)_DATABASE_URL', key)
  if match:
    vars()[match.group(1)] = Connection(os.environ.get(match.group()), autoconnect=autoconnect)
    vars()["connections"].append(match.group(1))
