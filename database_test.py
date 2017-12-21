import sqlite3

conn = sqlite3.connect('ocrfid.db')
events = ["build"]
c = conn.cursor()
c.execute('''SELECT sum(out_time), sum(in_time) FROM timesheet WHERE out_time!=-1 AND event IN (%s)''' % ','.join('?'*len(events)), events)

time = c.fetchone()
print (time[0] - time[1]) / 3600

conn.commit()
conn.close()
