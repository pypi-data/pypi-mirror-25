"""quickstep.py: Accesses the network command line interface of the quickstep database."""

import grpc
import pandas as pd
import quickstep.proto.NetworkCli_pb2 as NetworkCli_pb2
import quickstep.proto.NetworkCli_pb2_grpc as NetworkCli_pb2_grpc


def sql_to_table(query):
  """Runs an SQL query on the quickstep database.

  Runs the passed SQL query on the quickstep database set in quickstepIP and quickstepPort
  and returns the result in a panda data frame.

  Args:
      query: postgresql query string to pass to quickstep database.

  Returns:
      A panda data frame representation of the returned data.

  Raises:
      ValueError: The query execution returns an error.
  """
  responseText,error = sql_to_text(query)
  if "ERROR" in error:
    raise ValueError(error)

  data={}
  if(format=='table'):
    # Return for empty or malformed responses  (For instance an INSERT or UPDATE)
    if (not responseText or responseText[0] != "+"):
      return pd.DataFrame()

    # Split by newline's and skip first [0], third [2] and last entry from formatting
    rows = responseText.split("\n")[1:-1]

    # Split first row by '|' to get column names.
    # Skip the first and last result because they are before the first '|' and after the last '|'
    columnNames = rows[0].split("|")[1:-1]
    columnNames = map(unicode.strip, columnNames)  # strip whitespace
    rows = rows[1:]

    for columnName in columnNames:
      data[columnName] = [];

    for row in rows:
      if row[0] == "|":  # Avoids bad lines such as the "Time" at the very bottom
        temp = row.split("|")[1:-1]
        temp = map(unicode.strip, temp)  # strip whitespace
        for ind, columnName in enumerate(columnNames):
          data[columnName].append(temp[ind]);

  if (format == 'csv'):

    # Split by newline's and skip first [0], third [2] and last entry from formatting
    rows = responseText.split("\n")

    # Split first row by ',' to get column names.
    columnNames = rows[0].split(",")
    columnNames = [i[1:-1].replace('""','"') for i in columnNames]  # strip "quotes" and unescape them

    rows=rows[1:-1] #Skip header row and empty last row when processing rows

    for columnName in columnNames:
      data[columnName] = [];

    for row in rows:
      temp = row.split(",")
      temp = [i[1:-1].replace('""','"') for i in temp]  # strip "quotes" and unescape them
      for ind, columnName in enumerate(columnNames):
        data[columnName].append(temp[ind]);

  return pd.DataFrame(data)

ip="localhost"
port="3000"
format="csv"

def sql_to_text(queryString):
  """Runs an SQL query on the quickstep database.

  Runs the passed SQL query on the quickstep database set in quickstepIP and quickstepPort
  and returns the result string.

  Args:
      query: postgresql query string to pass to quickstep database.

  Returns:
      A string representation of the returned data and any errors returned from
      query execution.
  """
  channel = grpc.insecure_channel(ip+":"+port)
  stub = NetworkCli_pb2_grpc.NetworkCliStub(channel)
  response = stub.SendQuery(NetworkCli_pb2.QueryRequest(query=queryString))
  return response.query_result, response.error_result

def tables():
  """Runs an SQL query on the quickstep database and returns a list of tables.

  Runs a query on the quickstep database set in quickstepIP and quickstepPort
  and returns a list of tables in the database.

  Args:
      none

  Returns:
      A list of table name strings for tables in the quickstep database.

  Raises:
      ValueError: The query execution returns an error.
  """

  responseText, error = sql_to_text("\\d")
  if "ERROR" in error:
    raise ValueError(error)

  rows = responseText.split("\n")[4:-2]

  tables=[];

  for row in rows:
    table = row.split("|")
    if len(table)>0:
      tableName = table[0].strip()
      type = table[1].strip()
      blocks = table[2].strip()
      tables.append({"name":tableName,"type":type,"blocks":blocks})
  return tables

def columns(table):
  """Runs an SQL query on the quickstep database for a given table name and returns a list of columns.

  Runs a query on the quickstep database set in quickstepIP and quickstepPort
  and returns a list of columns in the given table.

  Args:
      table: Table name string to return columns for.

  Returns:
      A list of column dicts with properties "name" and "type".

  Raises:
      ValueError: The query execution returns an error.
  """
  responseText, error = sql_to_text("\\d " + table)
  if "ERROR" in error:
    raise ValueError(error)

  rows = responseText.split("\n")[3:-1]

  columns = [];

  for row in rows:
    column = row.split("|")
    if len(column) > 0:
      columnName = column[0].strip()
      dataType = column[1].strip()
      columns.append({"name":columnName,"type":dataType})
  return columns

def rows(table, count="ALL"):
  """Runs an SQL query for a given table name and returns a panda data frame with the table's data.

  Runs a query on the quickstep database set in quickstepIP and quickstepPort
  and returns a panda data frame with the table's data.

  Args:
      table: Table name string to return data for.
      count: The maximum number of rows to return.

  Returns:
      A panda data frame representation of the returned data.

  Raises:
      ValueError: The query execution returns an error.
  """
  limitString=((" LIMIT "+str(count)) if count!="ALL" else "")
  return sql_to_table("SELECT * FROM " + table + " ORDER BY " + columns(table)[0]["name"] + limitString + ";")