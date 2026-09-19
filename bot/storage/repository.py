import json,sqlite3,threading
from pathlib import Path
from datetime import datetime,timezone
class Repository:
    def __init__(self,url='sqlite:///./data/bot.db'):
        self.path=Path(url.removeprefix('sqlite:///')); self.path.parent.mkdir(parents=True,exist_ok=True); self.lock=threading.Lock()
    def _conn(self): return sqlite3.connect(self.path)
    def init(self):
        with self._conn() as c:
            c.execute('CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,kind TEXT NOT NULL,payload TEXT NOT NULL)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at DESC)')
    def log_event(self,kind,payload):
        with self.lock:
            with self._conn() as c:c.execute('INSERT INTO events(created_at,kind,payload) VALUES(?,?,?)',(datetime.now(timezone.utc).isoformat(),kind,json.dumps(payload)))
    def recent(self,limit=50):
        with self.lock:
            with self._conn() as c:return c.execute('SELECT kind,payload,created_at FROM events ORDER BY id DESC LIMIT ?',(limit,)).fetchall()
