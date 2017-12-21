import sqlite3

conn = sqlite3.connect('ocrfid.db')

c = conn.cursor()
c.execute('''CREATE TABLE settings (attribute text, value text)''')
c.execute('''INSERT INTO settings (attribute, value) VALUES(currentEvent, build)''')
c.execute('''INSERT INTO settings (attribute, value) VALUES(event, build)''')
c.execute('''CREATE TABLE members (uuid text, name text, register_time bigint)''')
c.execute('''CREATE TABLE timesheet (uuid text, event text, in_time bigint, out_time bigint)''')

conn.commit()
conn.close()
