#!/usr/bin/env python3
"""
Convert Zoom meeting config to WordPress events config.

This utility maps the Zoom config format used by create_zoom_recurring_meetings.py
to the events config format used by create_events.py.

Recurrence settings in Zoom are not converted to WordPress recurrence rules.
Each Zoom meeting entry maps to a single WordPress event occurrence.

Usage:
        python scripts/map_zoom_to_event_series_config.py \
            --zoom-config zoom-meeting-2026-config.json \
            --output events-config-from-zoom.json
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map Zoom meeting config to WordPress events config"
    )
    parser.add_argument(
        "--zoom-config",
        required=True,
        help="Path to source Zoom config JSON (e.g., zoom-meeting-2026-config.json)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path for output WordPress events JSON",
    )
    parser.add_argument(
        "--wordpress-url",
        default="https://your-wordpress-site.com",
        help="WordPress URL to place in output config",
    )
    parser.add_argument(
        "--username",
        default="your-username",
        help="WordPress username to place in output config",
    )
    parser.add_argument(
        "--app-password",
        default="xxxx xxxx xxxx xxxx xxxx xxxx",
        help="WordPress app password placeholder/value",
    )
    parser.add_argument(
        "--status",
        default="draft",
        choices=["draft", "publish"],
        help="Global event status in output config",
    )
    parser.add_argument(
        "--default-timezone",
        default="America/New_York",
        help="Fallback timezone when a Zoom meeting does not define one",
    )
    return parser.parse_args()


def compute_end_time(start_time: str, duration_minutes: int) -> str:
    start_dt = datetime.strptime(start_time, "%H:%M:%S")
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    return end_dt.strftime("%H:%M:%S")


def map_meeting_to_event(meeting: Dict[str, Any], default_timezone: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    start_date = meeting.get("start_date")
    if not start_date:
        return None, "missing start_date"

    start_time = meeting.get("start_time", "00:00:00")
    duration = int(meeting.get("duration", 60))

    event = {
        "title": meeting.get("topic", "Untitled Event"),
        "description": meeting.get("agenda", ""),
        "start_date": start_date,
        "end_date": start_date,
        "start_time": start_time,
        "end_time": compute_end_time(start_time, duration),
        "venue": "Virtual - Zoom",
        "organizer": meeting.get("host_email", ""),
        "categories": ["Collaboration Area", "Zoom Meeting"],
        "timezone": meeting.get("timezone", default_timezone),
    }

    recurrence_type = str(meeting.get("recurrence_type", "")).strip().lower()
    if recurrence_type and recurrence_type != "none":
        return event, "recurrence settings ignored; mapped as a single event"

    return event, None


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, payload: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def main() -> None:
    args = parse_args()

    try:
        zoom_config = load_json(args.zoom_config)
    except FileNotFoundError:
        print(f"Error: Zoom config file not found: {args.zoom_config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in Zoom config: {e}")
        sys.exit(1)

    meetings = zoom_config.get("meetings", [])
    if not meetings:
        print("Error: No 'meetings' found in Zoom config")
        sys.exit(1)

    events: List[Dict[str, Any]] = []
    warnings: List[str] = []

    for index, meeting in enumerate(meetings, start=1):
        event, warning = map_meeting_to_event(meeting, args.default_timezone)

        if event is None:
            topic = meeting.get("topic", "Untitled")
            warnings.append(f"Skipped meeting #{index} ('{topic}'): {warning}")
            continue

        if warning:
            topic = meeting.get("topic", "Untitled")
            warnings.append(f"Mapped meeting #{index} ('{topic}') with note: {warning}")

        events.append(event)

    output_payload = {
        "wordpress_url": args.wordpress_url,
        "username": args.username,
        "app_password": args.app_password,
        "status": args.status,
        "timezone": args.default_timezone,
        "events": events,
    }

    write_json(args.output, output_payload)

    print(f"✓ Wrote mapped config to: {args.output}")
    print(f"  Meetings read: {len(meetings)}")
    print(f"  Events mapped: {len(events)}")
    print(f"  Meetings skipped: {len(meetings) - len(events)}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")


if __name__ == "__main__":
    main()
