import sys
import os
from io import StringIO
import inspect
import re
import logging
import psycopg2
import psycopg2.extras
import pandas as pd

if sys.version_info.major < 3:
  from urlparse import urlparse
else:
  from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class Connection(object):

  def __init__(self, url, connect=True):
    self.__url = url
    self._adapter = None
    self._cursor = None
    if connect:
        self.connect()

  def __str__(self):
    parsed = urlparse(self.__url)
    return "Connection[{hostname}]:{port} > {user}@{dbname}".format(
      hostname=parsed.hostname, port=parsed.port, user=parsed.username, dbname=parsed.path[1:])

  def __repr__(self):
    return self.__str__()

  def connect(self):
    if self._adapter:
      return

    logger.info(self.__url)

    parsed = urlparse(self.__url)
    self._adapter = psycopg2.connect(
      database=parsed.path[1:],
      user=parsed.username,
      password=parsed.password,
      host=parsed.hostname,
      port=parsed.port,
      connect_timeout=1
    )
    self._adapter.autocommit = True
    self._cursor = self._adapter.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def close(self):
    if not self._adapter:
      return

    self._adapter.close()
    self._adapter = None
    self._cursor = None

  def dataframe(self, sql=None, filename=None, **kwargs):
    sql = self.__prepare(sql, filename, kwargs)
    dataframe = self._dataframe(sql=sql)
    buffer = StringIO()
    dataframe.info(buf=buffer, memory_usage='deep')
    logger.info(buffer.getvalue())
    logger.info(dataframe.head())
    return dataframe

  def _dataframe(self, sql):
    self.connect()
    sql = self._query_annotation(stack_depth=2) + sql
    print sql
    logger.debug(sql)
    return pd.io.sql.read_sql(sql=sql, con=self._adapter)

  def __prepare(self, sql, filename, bindings):
    if sql is None and filename is not None:
      logger.debug("READ SQL FILE: " + filename)
      with open(filename) as file:
        sql = file.read()
    sql = re.sub(r'\{(\w+?)\}', r'%(\1)s', sql)
    if self._cursor:
      cursor = self._cursor
    else:
      try:
        cursor = psycopg2.extras.DictCursor(conn=psycopg2.extensions.connection(dsn=''))
      except psycopg2.OperationalError:
        self.connect()
        cursor = self._cursor

    return cursor.mogrify(sql, bindings).decode('utf-8')

  def _query_annotation(self, stack_depth=3):
    caller = inspect.stack()[stack_depth]
    if sys.version_info.major == 3:
      caller = (caller.function, caller.filename, caller.lineno)
    return "/* %s | %s:%d in %s */\n" % (os.path.dirname(__file__), caller[1], caller[2], caller[0])
