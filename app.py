
from flask import Flask, request, g, session, render_template
import sqlite3
import time
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'something_secret_here'  # required for sessions

DATABASE = 'visitors.db'
ONLINE_TIMEOUT = 300  # 5 minutes

def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(DATABASE)
        g._database.row_factory = sqlite3.Row
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db:
        db.close()

@app.before_request
def track():
    # Skip tracking for static files
    if request.path.startswith('/static/'):
        return

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'unknown')
    now = time.time()
    timestamp = datetime.utcnow()

    # Assign a session_id if not present
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        session["visit_counted"] = False

    session_id = session["session_id"]
    db = get_db()
    cur = db.cursor()

    # Only log the visit if we haven't counted this session yet
    if not session.get("visit_counted", False):
        # Log the visit
        cur.execute("INSERT INTO visits (session_id, ip, user_agent, timestamp) VALUES (?, ?, ?, ?)",
                   (session_id, ip, user_agent, timestamp))
        session["visit_counted"] = True

    # Always update online status
    cur.execute("""
        INSERT OR REPLACE INTO online (session_id, ip, user_agent, last_seen)
        VALUES (?, ?, ?, ?)
    """, (session_id, ip, user_agent, now))

    # Remove expired online users
    cur.execute("DELETE FROM online WHERE last_seen < ?", (now - ONLINE_TIMEOUT,))
    db.commit()

@app.route('/')
def index():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM visits")
    total_visits = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM online")
    online_users = cur.fetchone()[0]

    return render_template("base.html", visited=total_visits, online=online_users)

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'),host="0.0.0.0")