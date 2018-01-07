import sqlite3

conn = sqlite3.connect('ocrfid.db')

c = conn.cursor()

c.execute('''DELETE FROM timesheet''')
#c.execute('''DELETE FROM members''')
#c.execute('''DELETE FROM settings WHERE attribute="event"''')
#c.execute('''INSERT INTO settings (attribute, value) VALUES("event", "Build 2018")''')

conn.commit()

conn.close()
