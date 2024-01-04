import sqlite3
import pandas as pd


# open the alerts database
def establishConnection(filePath):
    connection = sqlite3.connect(filePath)
    cur = connection.cursor()
    return connection

# get all values from the query in list of tuples
# Use pandas to read the SQL query result into a DataFrame
def getRecords(conn):
    pd.set_option('display.max_rows', None)
    df = pd.read_sql_query("SELECT alert_id, time,severity_level,ip_src,ip_dst,reason,filename FROM alerts", conn)
    recent_rows = df.tail(75)
    print(recent_rows.to_string(index=False))
    print('\n')

#prints a sorted data frame
def getRecordsSorted(conn, sort):
   try:
    querry = 'SELECT alert_id, time,severity_level,ip_src,ip_dst,reason,filename FROM alerts ORDER BY '+sort
    pd.set_option('display.max_rows', None)
    df = pd.read_sql_query(querry, conn)
    print(f"\n\n\n*****Alerts Sorted By: {sort}*****")
    recent_rows = df.tail(75)
    print(recent_rows.to_string(index=False))
    print('\n')
   except Exception as e:
      print('\ncolumn not found...\nPlease enter a valid sorting column\n')

def getRecordsFiltered(conn, filtered, value):
   try:
    querry = 'SELECT alert_id, time,severity_level,ip_src,ip_dst,reason,filename FROM alerts WHERE '+filtered+' = '+value
    pd.set_option('display.max_rows', None)
    df = pd.read_sql_query(querry, conn)
    print(f"\n\n\n*****Alerts Filtered By: {filtered} = {value}*****")
    recent_rows = df.tail(75)
    print(recent_rows.to_string(index=False))
    print('\n')
   except Exception as e:
      print('\nValue not found...\nPlease enter a valid filtering value\n')