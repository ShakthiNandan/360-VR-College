import sqlite3

conn = sqlite3.connect("visitors.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS visits (
    session_id TEXT,
    ip TEXT,
    user_agent TEXT,
    timestamp TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS online (
    session_id TEXT PRIMARY KEY,
    ip TEXT,
    user_agent TEXT,
    last_seen REAL
)
""")

conn.commit()
conn.close()

print("Database initialized.")
