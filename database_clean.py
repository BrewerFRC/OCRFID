import sqlite3

conn = sqlite3.connect('ocrfid.db')

c = conn.cursor()

c.execute('''DELETE FROM timesheet''')

conn.commit()

conn.close()
