#Event queries
get_events = '''SELECT DISTINCT value FROM settings WHERE attribute="event"'''
get_current_event = '''SELECT value FROM settings WHERE attribute="currentEvent"'''
create_event = '''INSERT INTO settings (attribute, value) VALUES("event", ?)'''

#Member queries
register_member = '''INSERT INTO members (uuid, name, register_time) VALUES (?, ?, ?)'''
get_members = '''SELECT DISTINCT uuid, name, register_time FROM members'''
get_uuid_by_name = '''SELECT uuid FROM members where name=?'''
check_member_exists = '''SELECT uuid FROM members WHERE uuid=?'''
update_name = '''UPDATE members SET name=?, register_time=? WHERE uuid=?'''

#Time clocking queries
get_clocks = '''SELECT (event, in_time, out_time) FROM timesheet WHERE uuid=?'''
get_clocks_by_event = '''SELECT out_time, in_time FROM timesheet WHERE uuid=? AND event IN '''
get_last_member_clock_out = '''SELECT max(out_time) FROM timesheet WHERE uuid=?'''
get_last_member_clock_out_by_event = '''SELECT max(out_time) FROM timesheet WHERE uuid=? AND out_time!=-1 AND event IN '''
clock_member = '''INSERT INTO timesheet (uuid, event, in_time, out_time) VALUES(?, ?, ?, ?)'''
check_for_open = '''SELECT in_time FROM timesheet WHERE uuid=? AND out_time=-1'''
cancel_open_member_clock = '''DELETE FROM timesheet WHERE uuid=? AND out_time=-1'''
close_clock = '''UPDATE timesheet SET out_time=? WHERE uuid=? AND out_time=-1'''
clear_member_clocks = '''DELETE FROM timesheet WHERE uuid=?'''
clear_open_clocks = '''DELETE FROM timesheet WHERE out_time=-1'''
