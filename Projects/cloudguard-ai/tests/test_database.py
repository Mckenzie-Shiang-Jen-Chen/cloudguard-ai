
import json
import sqlite3

from cloudguard.database import (
    initialize_database,
    insert_events
)
from cloudguard.normalization import normalize_event


def test_database_insert_and_duplicate(tmp_path):
    """Verify event storage and duplicate handling."""

    db_path = tmp_path / "test_cloudguard.db"

    initialize_database(db_path)

    raw_event = {
        "eventID": "test-001",
        "eventTime": "2026-10-26T10:00:00Z",
        "eventName": "ConsoleLogin",
        "eventSource": "signin.amazonaws.com",
        "sourceIPAddress": "192.0.2.10",
        "userIdentity": {
            "userName": "test-user"
        },
        "responseElements": {
            "ConsoleLogin": "Failure"
        }
    }

    normalized = normalize_event(raw_event)

    # First insertion should insert one row.
    inserted = insert_events(db_path, [normalized])
    assert inserted == 1

    # Inserting the same event again should add no rows.
    inserted_again = insert_events(db_path, [normalized])
    assert inserted_again == 0

    # Verify the stored data.
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "SELECT event_id, outcome, raw_json FROM events"
        ).fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "test-001"
    assert rows[0][1] == "Failure"
    assert json.loads(rows[0][2])["eventName"] == "ConsoleLogin"
