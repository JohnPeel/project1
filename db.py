
import cx_Oracle
import os


username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

hostname = os.getenv('SERVER_HOSTNAME', 'cise.dgby.org')
port = os.getenv('SERVER_PORT', 1521)
sid = os.getenv('SERVER_SID', 'orcl')
dsn = cx_Oracle.makedsn(hostname, port, sid)

conn = None


def get_conn():
    global conn
    if conn:
        return conn
    conn = cx_Oracle.connect(username, password, dsn)
    return conn


def get_cursor():
    return get_conn().cursor()


def query(x):
    for result in get_cursor().execure(x):
        yield result
