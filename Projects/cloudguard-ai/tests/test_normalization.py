
import pytest

from cloudguard.normalization import normalize_event


def test_failed_login():
    """Ensure failed console logins are identified."""

    event = {
        "eventID": "test-001",
        "eventName": "ConsoleLogin",
        "userIdentity": {
            "type": "IAMUser",
            "userName": "test-user"
        },
        "sourceIPAddress": "192.0.2.10",
        "responseElements": {
            "ConsoleLogin": "Failure"
        }
    }

    result = normalize_event(event)

    assert result["event_name"] == "ConsoleLogin"
    assert result["principal"] == "test-user"
    assert result["outcome"] == "Failure"
    assert result["source_ip"] == "192.0.2.10"


def test_successful_login():
    """Ensure successful console logins are identified."""

    event = {
        "eventID": "test-002",
        "eventName": "ConsoleLogin",
        "responseElements": {
            "ConsoleLogin": "Success"
        }
    }

    result = normalize_event(event)

    assert result["outcome"] == "Success"


def test_api_error():
    """Ensure AWS API errors are recorded as failures."""

    event = {
        "eventID": "test-003",
        "eventName": "CreateUser",
        "errorCode": "AccessDenied"
    }

    result = normalize_event(event)

    assert result["outcome"] == "Failure"


def test_missing_event_id():
    """Reject events that lack an event ID."""

    event = {
        "eventName": "ConsoleLogin"
    }

    with pytest.raises(ValueError):
        normalize_event(event)


def test_principal_arn_fallback():
    """Use the ARN when a username is unavailable."""

    event = {
        "eventID": "test-004",
        "eventName": "CreateUser",
        "userIdentity": {
            "arn": "arn:aws:iam::123456789012:role/demo-role"
        }
    }

    result = normalize_event(event)

    assert result["principal"] == (
        "arn:aws:iam::123456789012:role/demo-role"
    )


def test_no_error_is_not_confirmed_success():
    """Missing an error does not prove an API call succeeded."""

    event = {
        "eventID": "test-005",
        "eventName": "StopLogging"
    }

    result = normalize_event(event)

    assert result["outcome"] == "No error recorded"
