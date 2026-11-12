from collections import Counter
from datetime import datetime

from cloudguard.ingestion import load_cloudtrail_logs
from cloudguard.normalization import normalize_event

def main():
    path = "data/samples/cloudtrail_sample.json"
    raw_events = load_cloudtrail_logs(path)
    if not raw_events:
        raise ValueError("dataset is empty")

    event_ids = set()
    event_types = Counter()

    for index, raw_event in enumerate(raw_events, start=1):
        event = normalize_event(raw_event)

        event_id = event["event_id"]
        if event_id in event_ids:
            raise ValueError(f"duplicated event id: {event_id}")

        event_ids.add(event_id)

        for field in ("event_time", "event_name", "event_source"):
            value = event[field]
            if not isinstance(value, str) or value in ("", "Unknown"):
                raise ValueError(
                    f"Event {index}: missing or invalid {field}"
                )

        try:
            datetime.fromisoformat(
                event["event_time"].replace("Z", "+00:00")
            )
        except ValueError as error:
            raise ValueError(
                f"Event {index}: invalid timestamp"
            ) from error

        event_types[event["event_name"]] += 1

    if len(raw_events) != len(event_ids):
        raise ValueError("Duplicate event IDs detected.")

    print("CloudGuard AI Dataset Validation")
    print("-" * 40)
    print(f"Total events: {len(raw_events)}")
    print(f"Unique event IDs: {len(event_ids)}")
    print("Event types:")

    for event_name, count in sorted(event_types.items()):
        print(f"  {event_name}: {count}")

    print("Dataset validation PASSED!")

if __name__ == "__main__":
    main()