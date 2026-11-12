from cloudguard.ingestion import load_cloudtrail_logs
from cloudguard.normalization import normalize_event
from cloudguard.database import initialize_database, insert_events

def main():
    log_path = "data/samples/cloudtrail_sample.json"
    db_path = "data/cloudguard.db"

    events = load_cloudtrail_logs(log_path) # load origianl cloudtrail logs

    normalize_events = [normalize_event(event) for event in events] # normalized each event

    initialize_database(db_path) # initialize database

    inserted = insert_events(db_path, normalize_events) # stored normalized event

    print(f"loaded {len(events)} cloudtrail events")
    print(f"inserted {inserted} new events into SQLite")

    for event in normalize_events:
        print("-" * 40)
        print(f"Event: {event['event_name']}")
        print(f"Principal: {event['principal']}")
        print(f"IP: {event['source_ip']}")
        print(f"Outcome: {event['outcome']}")

if __name__ == "__main__":
    main()