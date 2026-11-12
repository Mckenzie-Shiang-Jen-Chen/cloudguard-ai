
import json
import pytest

from cloudguard.ingestion import load_cloudtrail_logs


def test_load_valid_logs(tmp_path):
    """Check that valid CloudTrail events can be loaded."""

    sample = {
        "Records": [
            {"eventID": "test-001"},
            {"eventID": "test-002"}
        ]
    }

    file_path = tmp_path / "test_logs.json"
    file_path.write_text(json.dumps(sample), encoding="utf-8")

    events = load_cloudtrail_logs(file_path)

    assert len(events) == 2
    assert events[0]["eventID"] == "test-001"


def test_missing_records(tmp_path):
    """Reject JSON without a Records array."""

    file_path = tmp_path / "invalid_logs.json"
    file_path.write_text('{"invalid": []}', encoding="utf-8")

    with pytest.raises(ValueError):
        load_cloudtrail_logs(file_path)


def test_invalid_json(tmp_path):
    """Reject malformed JSON data."""

    file_path = tmp_path / "broken.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_cloudtrail_logs(file_path)


def test_invalid_record_type(tmp_path):
    """Reject a Records array containing non-object entries."""

    file_path = tmp_path / "bad_records.json"
    file_path.write_text(
        '{"Records": [null]}',
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        load_cloudtrail_logs(file_path)
