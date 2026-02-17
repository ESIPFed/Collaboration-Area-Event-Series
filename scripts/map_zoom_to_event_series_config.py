#!/usr/bin/env python3
"""
Convert Zoom recurring meeting config to WordPress event-series config.

This utility maps the Zoom config format used by create_zoom_recurring_meetings.py
to the event-series format used by create_recurring_events.py.

Supported mapping:
- Zoom monthly recurrence using monthly_week + monthly_week_day

Unsupported entries are skipped with warnings (for example weekly recurrence).

Usage:
    python scripts/map_zoom_to_event_series_config.py \
      --zoom-config zoom-meeting-2026-config.json \
      --output event-series-config-from-zoom.json
"""

import argparse
import json
import calendar
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple


POSITION_MAP = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    -1: "last",
}

WEEKDAY_MAP = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map Zoom meeting config to WordPress event-series config"
    )
    parser.add_argument(
        "--zoom-config",
        required=True,
        help="Path to source Zoom config JSON (e.g., zoom-meeting-2026-config.json)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path for output WordPress event-series JSON",
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


def is_last_weekday_of_month(date_obj: datetime.date) -> bool:
    _, month_days = calendar.monthrange(date_obj.year, date_obj.month)
    return (date_obj.day + 7) > month_days


def recurrence_day_from_start_date(start_date: str) -> str:
    date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    weekday_name = date_obj.strftime("%A")

    if is_last_weekday_of_month(date_obj):
        position = "last"
    else:
        week_num = ((date_obj.day - 1) // 7) + 1
        position = POSITION_MAP.get(week_num, "first")

    return f"{position} {weekday_name}"


def map_recurrence_day(meeting: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    recurrence_type = meeting.get("recurrence_type", "monthly").lower()

    if recurrence_type != "monthly":
        return None, f"unsupported recurrence_type='{recurrence_type}'"

    monthly_week = meeting.get("monthly_week")
    monthly_week_day = meeting.get("monthly_week_day")

    if monthly_week in POSITION_MAP and monthly_week_day in WEEKDAY_MAP:
        return f"{POSITION_MAP[monthly_week]} {WEEKDAY_MAP[monthly_week_day]}", None

    if "start_date" in meeting:
        return recurrence_day_from_start_date(meeting["start_date"]), (
            "monthly pattern missing monthly_week/monthly_week_day; "
            "derived recurrence_day from start_date"
        )

    return None, "missing monthly_week/monthly_week_day and start_date"


def map_meeting_to_event(meeting: Dict[str, Any], default_timezone: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    recurrence_day, recurrence_warning = map_recurrence_day(meeting)
    if recurrence_day is None:
        return None, recurrence_warning

    start_time = meeting.get("start_time", "00:00:00")
    duration = int(meeting.get("duration", 60))

    event = {
        "title": meeting.get("topic", "Untitled Event"),
        "description": meeting.get("agenda", ""),
        "start_date": meeting.get("start_date", ""),
        "end_date": meeting.get("end_date", meeting.get("start_date", "")),
        "start_time": start_time,
        "end_time": compute_end_time(start_time, duration),
        "recurrence_pattern": "MONTHLY",
        "recurrence_day": recurrence_day,
        "venue": "Virtual - Zoom",
        "organizer": meeting.get("host_email", ""),
        "categories": ["Collaboration Area", "Zoom Meeting"],
        "timezone": meeting.get("timezone", default_timezone),
    }

    if recurrence_warning:
        return event, recurrence_warning
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
