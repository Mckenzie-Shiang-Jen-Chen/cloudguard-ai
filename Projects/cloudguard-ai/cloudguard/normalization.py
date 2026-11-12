import json

def normalize_event(event):
    """Convert a cloudtrail event to standard structure"""

    if not isinstance(event, dict):
        raise ValueError("Cloudtrail event must be an object")

    event_id = event.get("eventID")

    if not isinstance(event_id, str) or not event_id.strip():
        raise ValueError("Cloudtrail event is missing eventID")

    identity = event.get("userIdentity") or {}
    response = event.get("responseElements") or {}
    if not isinstance(identity, dict):
        identity = {}
    if not isinstance(response, dict):
        response = {}

    event_name = event.get("eventName", "Unknown")
    principal = (
        identity.get("userName")
        or identity.get("arn")
        or identity.get("principalId")
        or "Unknown"
    )

    if event_name == "ConsoleLogin" and response.get("ConsoleLogin"):
        outcome = response["ConsoleLogin"]
    elif event.get("errorCode"):
        outcome = "Failure"
    else:
        outcome = "No error recorded"

    return {
        "event_id": event_id,
        "event_time": event.get("eventTime", "Unknown"),
        "event_name": event_name,
        "event_source": event.get("eventSource", "Unknown"),
        "principal": principal,
        "source_ip": event.get("sourceIPAddress", "Unknown"),
        "aws_region": event.get("awsRegion", "Unknown"),
        "outcome": outcome,
        "raw_json": json.dumps(event)
    }