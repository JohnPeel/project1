import db
import cx_Oracle
import json
import pprint


def simple_select(table, selector, **constraints):
    c = ''
    for key, value in constraints.items():
        c += "%s='%s' AND " % (key, value)
    c = c[:-5]

    query = 'SELECT %s FROM %s WHERE %s' % (selector, table, c)
    try:
        return db.get_cursor().execute(query).fetchall()
    except cx_Oracle.DatabaseError:
        print('ERROR: %s' % query)


pprint.pprint(json.dumps(simple_select('GAME', '*', season='2011', week='2')))


x = 0
if x is int:
    print(True)
