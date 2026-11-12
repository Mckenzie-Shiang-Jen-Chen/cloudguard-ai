import sqlite3
from pathlib import Path

def initialize_database(db_path):
    """Create the SQLite database and events table"""

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        connection.execute(""" 
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                event_time TEXT,
                event_name TEXT,
                event_source TEXT,
                principal TEXT,
                source_ip TEXT,
                aws_region TEXT,
                outcome TEXT,
                raw_json TEXT NOT NULL
            )
        """)

def insert_events(db_path, events):
    """Insert normalized events without duplicating event IDs"""

    with sqlite3.connect(db_path) as connection:
        before = connection.total_changes

        for event in events:
            connection.execute("""
                INSERT OR IGNORE INTO events (
                event_id,
                event_time,
                event_name,
                event_source,
                principal,
                source_ip,
                aws_region,
                outcome,
                raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event["event_id"],
                event["event_time"],
                event["event_name"],
                event["event_source"],
                event["principal"],
                event["source_ip"],
                event["aws_region"],
                event["outcome"],
                event["raw_json"]
            ))

        return connection.total_changes - before