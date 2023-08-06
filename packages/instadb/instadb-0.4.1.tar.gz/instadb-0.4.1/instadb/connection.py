import sys
from io import StringIO
import inspect
import re
import logging
import psycopg2
import psycopg2.extras
import pandas as pd
from util import retry

if sys.version_info.major < 3:
  from urlparse import urlparse
else:
  from urllib.parse import urlparse

MAX_CONNECT_RETRIES = 3

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

  def __logger(self):
    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    return logging.getLogger(__name__)

  @retry(psycopg2.OperationalError, tries=MAX_CONNECT_RETRIES)
  def connect(self):
    if self._adapter:
      return

    parsed = urlparse(self.__url)
    self._adapter = psycopg2.connect(
      connection_factory=psycopg2.extras.MinTimeLoggingConnection,
      database=parsed.path[1:],
      user=parsed.username,
      password=parsed.password,
      host=parsed.hostname,
      port=parsed.port,
      connect_timeout=5
    )
    self._adapter.initialize(self.__logger())
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
    sql = self._query_annotation(stack_depth=2) + sql
    dataframe = self._dataframe(sql=sql)
    buffer = StringIO()
    dataframe.info(buf=buffer, memory_usage='deep')
    self.__logger().info(buffer.getvalue())
    self.__logger().info(dataframe.head())
    return dataframe

  def _dataframe(self, sql):
    self.connect()
    return pd.io.sql.read_sql(sql=sql, con=self._adapter)

  def __prepare(self, sql, filename, bindings):
    if sql is None and filename is not None:
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

  def _query_annotation(self, stack_depth=2):
    caller = inspect.stack()[stack_depth]
    if sys.version_info.major == 3:
      caller = (caller.function, caller.filename, caller.lineno)
    return "/* %s:%d */\n" % (caller[1], caller[2])
