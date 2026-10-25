import sqlite3

conn = sqlite3.connect('helpdesk.db')
cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS tickets
""")

cursor.execute("""
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_no TEXT,
    store TEXT,
    asset_name TEXT,
    issue_category TEXT,
    priority TEXT,
    issue_description TEXT,
    status TEXT,
    date_opened TEXT,
    assigned_to TEXT
)
""")

conn.commit()
conn.close()

print("Database Updated")
