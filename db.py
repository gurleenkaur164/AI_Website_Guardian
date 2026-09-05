import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("GUARDIAN_DB", "guardian.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            intent TEXT NOT NULL,
            severity TEXT DEFAULT 'low',
            original_message TEXT NOT NULL,
            action_taken TEXT,
            agent_notes TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(intent, message, severity="low", action_taken="", agent_notes=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (timestamp, intent, severity, original_message, action_taken, agent_notes) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), intent, severity, message, action_taken, agent_notes)
    )
    conn.commit()
    conn.close()

def search_similar(keyword):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, timestamp, intent, severity, original_message FROM messages WHERE original_message LIKE ? ORDER BY timestamp DESC LIMIT 5",
        (f"%{keyword}%",)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent(intent=None, limit=10):
    conn = get_connection()
    if intent:
        rows = conn.execute(
            "SELECT id, timestamp, intent, severity, original_message, action_taken FROM messages WHERE intent = ? ORDER BY timestamp DESC LIMIT ?",
            (intent, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, timestamp, intent, severity, original_message, action_taken FROM messages WHERE 1=1 ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats():
    conn = get_connection()
    intent_counts = conn.execute(
        "SELECT intent, COUNT(*) as count FROM messages GROUP BY intent ORDER BY count DESC"
    ).fetchall()
    severity_counts = conn.execute(
        "SELECT severity, COUNT(*) as count FROM messages GROUP BY severity ORDER BY count DESC"
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) as count FROM messages").fetchone()["count"]
    conn.close()
    return {
        "total": total,
        "by_intent": {r["intent"]: r["count"] for r in intent_counts},
        "by_severity": {r["severity"]: r["count"] for r in severity_counts},
    }

init_db()
