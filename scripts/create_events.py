#!/usr/bin/env python3
"""
Create one or more non-recurring events using The Events Calendar Pro REST API.

This script intentionally does not send recurrence rules because recurring event
creation is not currently supported through the Events Calendar Pro REST API.

Usage:
    python scripts/create_events.py --config path/to/config.json
    python scripts/create_events.py --config path/to/config.json --dry-run
"""

import argparse
import json
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create single or multiple non-recurring events in WordPress",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_help_epilog(),
    )
    parser.add_argument("--config", required=True, help="Path to JSON configuration file")
    parser.add_argument("--dry-run", action="store_true", help="Show payload(s) without creating events")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    config = load_config(args.config)
    if config is None:
        sys.exit(1)

    events = extract_events(config)
    if not validate_config(config, events):
        sys.exit(1)

    create_events(config=config, events=events, dry_run=args.dry_run, verbose=args.verbose)


def get_help_epilog() -> str:
    return """
Configuration file supports either a single "event" object or an "events" array.

Example with multiple events:
{
  "wordpress_url": "https://your-site.com",
  "username": "your-username",
  "app_password": "your-app-password",
  "status": "draft",
  "timezone": "America/New_York",
  "events": [
    {
      "title": "Event One",
      "description": "Description",
      "start_date": "2026-03-01",
      "end_date": "2026-03-01",
      "start_time": "14:00:00",
      "end_time": "15:00:00",
      "venue": "Virtual",
      "organizer": "My Organization",
      "categories": ["Category1"]
    }
  ]
}

Example with one event:
{
  "wordpress_url": "https://your-site.com",
  "username": "your-username",
  "app_password": "your-app-password",
  "event": {
    "title": "Single Event",
    "start_date": "2026-03-01",
    "end_date": "2026-03-01",
    "start_time": "14:00:00",
    "end_time": "15:00:00"
  }
}
"""


def load_config(config_path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}")
        return None
    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON in config file: {error}")
        return None


def extract_events(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "events" in config:
        events = config["events"]
        return events if isinstance(events, list) else []

    if "event" in config and isinstance(config["event"], dict):
        return [config["event"]]

    return []


def validate_config(config: Dict[str, Any], events: List[Dict[str, Any]]) -> bool:
    required_fields = ["wordpress_url", "username", "app_password"]
    for field in required_fields:
        if field not in config:
            print(f"Error: Missing required field '{field}' in config")
            return False

    if not events:
        print("Error: Config must include either a non-empty 'events' array or an 'event' object")
        return False

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            print(f"Error: Event at index {index} must be an object")
            return False

        event_required = ["title", "start_date", "end_date", "start_time", "end_time"]
        for field in event_required:
            if field not in event:
                print(f"Error: Event {index} missing required field '{field}'")
                return False

        if not validate_date(event["start_date"]):
            print(f"Error: Event {index} has invalid start_date '{event['start_date']}' (expected YYYY-MM-DD)")
            return False
        if not validate_date(event["end_date"]):
            print(f"Error: Event {index} has invalid end_date '{event['end_date']}' (expected YYYY-MM-DD)")
            return False
        if not validate_time(event["start_time"]):
            print(f"Error: Event {index} has invalid start_time '{event['start_time']}' (expected HH:MM:SS)")
            return False
        if not validate_time(event["end_time"]):
            print(f"Error: Event {index} has invalid end_time '{event['end_time']}' (expected HH:MM:SS)")
            return False

        start_dt = parse_datetime(event["start_date"], event["start_time"])
        end_dt = parse_datetime(event["end_date"], event["end_time"])
        if start_dt is None or end_dt is None:
            print(f"Error: Event {index} has invalid start/end date-time")
            return False
        if end_dt <= start_dt:
            print(f"Error: Event {index} end date-time must be after start date-time")
            return False

    return True


def validate_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_time(value: str) -> bool:
    try:
        datetime.strptime(value, "%H:%M:%S")
        return True
    except ValueError:
        return False


def parse_datetime(date_value: str, time_value: str) -> Optional[datetime]:
    try:
        return datetime.strptime(f"{date_value} {time_value}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def create_events(config: Dict[str, Any], events: List[Dict[str, Any]], dry_run: bool, verbose: bool) -> None:
    wp_url = config["wordpress_url"].rstrip("/")
    api_url = f"{wp_url}/wp-json/tribe/events/v1/events"
    auth: Tuple[str, str] = (config["username"], config["app_password"])

    print("Creating non-recurring events...")
    print(f"WordPress URL: {wp_url}")
    print(f"Number of events to process: {len(events)}")

    if dry_run:
        print("\n*** DRY RUN MODE - No events will be created ***\n")

    success_count = 0
    failure_count = 0

    for index, event_data in enumerate(events):
        print(f"Processing event {index + 1}: {event_data['title']}")
        payload = build_event_payload(event_data, config)

        if dry_run:
            print("  [DRY RUN] Would create event with payload:")
            print(json.dumps(payload, indent=2))
            success_count += 1
            print()
            continue

        event_id, error = create_event(api_url, auth, payload, verbose)
        if event_id is not None:
            print(f"  ✓ Successfully created event ID: {event_id}")
            success_count += 1
        else:
            print(f"  ✗ Failed to create event: {error}")
            failure_count += 1

        print()
        time.sleep(0.5)

    print("Summary:")
    print(f"  Successfully processed: {success_count}")
    print(f"  Failed: {failure_count}")


def build_event_payload(event_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    status = event_data.get("status", config.get("status", "draft"))
    timezone = event_data.get("timezone", config.get("timezone", "America/New_York"))
    payload: Dict[str, Any] = {
        "title": event_data["title"],
        "description": event_data.get("description", ""),
        "status": status,
        "start_date": f"{event_data['start_date']} {event_data['start_time']}",
        "end_date": f"{event_data['end_date']} {event_data['end_time']}",
        "all_day": bool(event_data.get("all_day", False)),
        "timezone": timezone,
    }

    if "venue" in event_data:
        payload["venue"] = {"venue": event_data["venue"]}

    if "organizer" in event_data:
        payload["organizer"] = {"organizer": event_data["organizer"]}

    if "categories" in event_data:
        payload["categories"] = event_data["categories"]

    return payload


def create_event(api_url: str, auth: Tuple[str, str], payload: Dict[str, Any], verbose: bool) -> Tuple[Optional[int], Optional[str]]:
    try:
        response = requests.post(
            api_url,
            json=payload,
            auth=auth,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        if verbose:
            print(f"  Response status: {response.status_code}")
            try:
                print(f"  Response body: {json.dumps(response.json(), indent=2)}")
            except ValueError:
                print(f"  Response body: {response.text}")

        if response.status_code in (200, 201):
            result = response.json()
            return result.get("id"), None

        response_code: Optional[str] = None
        try:
            response_json = response.json()
            response_code = response_json.get("code")
        except ValueError:
            response_json = None

        if response_code == "could-not-create-organizer" and "organizer" in payload:
            retry_payload = dict(payload)
            retry_payload.pop("organizer", None)

            if verbose:
                print("  Organizer creation failed; retrying without organizer field...")

            retry_response = requests.post(
                api_url,
                json=retry_payload,
                auth=auth,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if verbose:
                print(f"  Retry response status: {retry_response.status_code}")
                try:
                    print(f"  Retry response body: {json.dumps(retry_response.json(), indent=2)}")
                except ValueError:
                    print(f"  Retry response body: {retry_response.text}")

            if retry_response.status_code in (200, 201):
                retry_result = retry_response.json()
                return retry_result.get("id"), None

        return None, f"HTTP {response.status_code} - {response.text}"
    except requests.RequestException as error:
        return None, str(error)


if __name__ == "__main__":
    main()