import json
from pathlib import Path

def load_cloudtrail_logs(file_path):
    """Load AWS CloudTrail events from json file"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")

    events = data.get("Records")
    if not isinstance(events, list):
        raise ValueError("expected a records array")

    if not all(isinstance(event, dict) for event in events):
        raise ValueError("each record must be a JSON object")

    return events

def display_events(events):
    """display information for each event"""

    for event in events:
        identity = event.get("userIdentity") or {}
        response = event.get("responseElements") or {}

        username = identity.get("userName", "Unknown")
        event_name = event.get("eventName", "Unknown")
        event_time = event.get("eventTime", "Unknown")
        source_ip = event.get("sourceIPAddress", "Unknown")

        if event_name == "ConsoleLogin":
            outcome = response.get("ConsoleLogin", "Unknown")
        elif event.get("errorCode"):
            outcome = "Failure"
        else:
            outcome = "No error recorded"

        print("-" * 45)
        print(f"User: {username}")
        print(f"Event: {event_name}")
        print(f"Time: {event_time}")
        print(f"Source IP: {source_ip}")
        print(f"Outcome: {outcome}")

if __name__ == "__main__":
    file_path = Path("data/samples/cloudtrail_sample.json")
    events = load_cloudtrail_logs(file_path)
    print(f"Load {len(events)} CloudTrail events")

    display_events(events)