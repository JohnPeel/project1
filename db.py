
import cx_Oracle
import os


username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

hostname = os.getenv('SERVER_HOSTNAME', 'cise.dgby.org')
port = os.getenv('SERVER_PORT', 1521)
sid = os.getenv('SERVER_SID', 'orcl')
dsn = cx_Oracle.makedsn(hostname, port, sid)

conn = None


def try_connection():
    return get_conn() and is_connected()


def is_connected():
    global conn
    try:
        return conn and conn.ping() is None
    except (cx_Oracle.InterfaceError, cx_Oracle.OperationalError):
        return False


def get_conn():
    global conn
    if conn and is_connected():
        return conn

    conn = cx_Oracle.connect(username, password, dsn)
    return conn


def get_cursor():
    return get_conn().cursor()


