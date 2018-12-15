import sqlite3

connection = sqlite3.connect('ocrfid.db')

def execute(SQL, arguments=None):
    cur = connection.cursor()
    if arguments:
        cur.execute(SQL, arguments)
    else:
        cur.execute(SQL)
    connection.commit()
    cur.close()

def fetchOne(SQL, arguments=None):
    cur = connection.cursor()
    if arguments:
        cur.execute(SQL, arguments)
    else:
        cur.execute(SQL)
    results = cur.fetchone()
    cur.close()
    return results

def fetchAll(SQL, arguments=None):
    cur = connection.cursor()
    if arguments:
        cur.execute(SQL, arguments)
    else:
        cur.execute(SQL)
    results = cur.fetchall()
    cur.close()

    return results
