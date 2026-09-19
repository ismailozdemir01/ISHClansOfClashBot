import sqlite3
from pathlib import Path
from datetime import datetime,timezone
class Repository:
    def __init__(self,url): self.path=Path(url.removeprefix("sqlite:///")); self.path.parent.mkdir(parents=True,exist_ok=True)
    def _conn(self): return sqlite3.connect(self.path)
    def init(self):
        with self._conn() as c:
            c.execute("CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY AUTOINCREMENT,started_at TEXT NOT NULL,ended_at TEXT,attacks INTEGER DEFAULT 0,searches INTEGER DEFAULT 0,errors INTEGER DEFAULT 0)")
            c.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,kind TEXT NOT NULL,payload TEXT NOT NULL)")
    def log_event(self,kind,payload):
        with self._conn() as c:c.execute("INSERT INTO events(created_at,kind,payload) VALUES(?,?,?)",(datetime.now(timezone.utc).isoformat(),kind,payload))
