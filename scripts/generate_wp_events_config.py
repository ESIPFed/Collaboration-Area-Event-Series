#!/usr/bin/env python3
"""
Generate a WordPress events config JSON from Zoom meeting config and Zoom output CSV.

This script:
- Uses examples/events-config.json as the output framework template
- Reads meetings from zoom meeting config JSON
- Looks up registration links from zoom_meetings_output.csv
- Writes wp-events-2026-config.json by default

Transform rules:
- Event title removes trailing " - 2026"
- Event description becomes the provided HTML block with:
  - CLUSTER NAME => cleaned title
  - REGISTRATION LINK FROM ZOOM => matched registration_url from CSV
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List


DESCRIPTION_TEMPLATE = """<div class=\"registration-container\">\n<h2 class=\"headline\">{cluster_name} 2026 Registration</h2>\n<p class=\"registration-note\"><strong>ESIP meetings are open to all</strong> who wish to participate and contribute. To ensure a secure and collaborative environment for all attendees, <strong>registration is required</strong> for each meeting series. Once registered, you will have immediate access to the join links for all upcoming sessions.</p>\n<a class=\"my-custom-button\" href=\"{registration_url}\">Click to register for the series</a>\n<p class=\"footer-note\">After registering, Zoom will email you a confirmation with a calendar invitation for the entire series. Use the <strong>\"Add to Calendar\"</strong> link to save the dates and your unique join link. <strong>Note:</strong> If a meeting time changes, you will receive an updated email. Because Zoom cannot auto-update your private calendar, please delete the old entry and use the new link to refresh your schedule.</p>\n<p class=\"annual-reset-note\"><strong>Note on Annual Registration:</strong> Your registration is valid for all meetings within the <strong>current calendar year</strong>. To maintain a secure environment and ensure our community lists are up-to-date, we perform an annual reset each January. You will be invited to re-register for your preferred Collaboration Areas at the start of the new year.</p>\n\n</div>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate WordPress events config from Zoom inputs")
    parser.add_argument(
        "--template",
        default="examples/events-config.json",
        help="Template framework config (default: examples/events-config.json)",
    )
    parser.add_argument(
        "--zoom-config",
        default="",
        help="Zoom meetings config JSON. If omitted, tries zoom-meetings-2026-config.json then zoom-meeting-2026-config.json",
    )
    parser.add_argument(
        "--zoom-output-csv",
        default="zoom_meetings_output.csv",
        help="Zoom output CSV containing registration_url (default: zoom_meetings_output.csv)",
    )
    parser.add_argument(
        "--output",
        default="wp-events-2026-config.json",
        help="Output WordPress events config path (default: wp-events-2026-config.json)",
    )
    return parser.parse_args()


def resolve_zoom_config_path(user_value: str) -> Path:
    if user_value:
        candidate = Path(user_value)
        if not candidate.exists():
            raise FileNotFoundError(f"Zoom config not found: {candidate}")
        return candidate

    candidates = [
        Path("zoom-meetings-2026-config.json"),
        Path("zoom-meeting-2026-config.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Could not find zoom config. Tried: zoom-meetings-2026-config.json, zoom-meeting-2026-config.json"
    )


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def clean_title(topic: str) -> str:
    return re.sub(r"\s*-\s*2026\s*$", "", topic).strip()


def calculate_end_time(start_time: str, duration_minutes: int) -> str:
    start_dt = datetime.strptime(start_time, "%H:%M:%S")
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    return end_dt.strftime("%H:%M:%S")


def build_registration_lookup(csv_rows: List[Dict[str, str]]) -> Dict[str, List[str]]:
    lookup: Dict[str, List[str]] = {}
    for row in csv_rows:
        topic = (row.get("meeting_topic") or "").strip()
        url = (row.get("registration_url") or "").strip()
        if not topic or not url:
            continue
        lookup.setdefault(topic, []).append(url)
    return lookup


def get_registration_url(topic: str, lookup: Dict[str, List[str]], usage: Dict[str, int]) -> str:
    urls = lookup.get(topic, [])
    if not urls:
        return ""

    index = usage.get(topic, 0)
    if index >= len(urls):
        index = len(urls) - 1

    usage[topic] = usage.get(topic, 0) + 1
    return urls[index]


def build_output_config(
    template_config: Dict[str, Any],
    zoom_config: Dict[str, Any],
    registration_lookup: Dict[str, List[str]],
) -> Dict[str, Any]:
    meetings = zoom_config.get("meetings", [])
    if not isinstance(meetings, list):
        raise ValueError("Invalid zoom config: 'meetings' must be a list")

    template_events = template_config.get("events", [])
    event_defaults: Dict[str, Any] = {}
    if isinstance(template_events, list) and template_events and isinstance(template_events[0], dict):
        event_defaults = dict(template_events[0])

    for key in ["title", "description", "start_date", "end_date", "start_time", "end_time"]:
        event_defaults.pop(key, None)

    output: Dict[str, Any] = {
        "wordpress_url": template_config.get("wordpress_url", "https://your-site.com"),
        "username": template_config.get("username", "admin"),
        "app_password": template_config.get("app_password", "your-application-password-here"),
        "status": template_config.get("status", "draft"),
        "timezone": template_config.get("timezone", "America/New_York"),
        "events": [],
    }

    usage: Dict[str, int] = {}

    for meeting in meetings:
        topic = str(meeting.get("topic", "")).strip()
        if not topic:
            continue

        start_date = str(meeting.get("start_date", "")).strip()
        start_time = str(meeting.get("start_time", "")).strip() or "00:00:00"
        duration = int(meeting.get("duration", 60))

        event_title = clean_title(topic)
        registration_url = get_registration_url(topic, registration_lookup, usage)

        event: Dict[str, Any] = dict(event_defaults)
        event.update(
            {
                "title": event_title,
                "description": DESCRIPTION_TEMPLATE.format(
                    cluster_name=event_title,
                    registration_url=registration_url,
                ),
                "start_date": start_date,
                "end_date": start_date,
                "start_time": start_time,
                "end_time": calculate_end_time(start_time, duration),
                "timezone": meeting.get("timezone", output["timezone"]),
            }
        )

        output["events"].append(event)

    return output


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)
        file.write("\n")


def main() -> None:
    args = parse_args()

    template_path = Path(args.template)
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    zoom_config_path = resolve_zoom_config_path(args.zoom_config)
    zoom_csv_path = Path(args.zoom_output_csv)
    if not zoom_csv_path.exists():
        raise FileNotFoundError(f"Zoom output CSV not found: {zoom_csv_path}")

    template_config = load_json(template_path)
    zoom_config = load_json(zoom_config_path)
    csv_rows = load_csv_rows(zoom_csv_path)

    registration_lookup = build_registration_lookup(csv_rows)
    output_config = build_output_config(template_config, zoom_config, registration_lookup)

    output_path = Path(args.output)
    write_json(output_path, output_config)

    print(f"✓ Wrote {len(output_config['events'])} events to {output_path}")
    print(f"  template: {template_path}")
    print(f"  zoom config: {zoom_config_path}")
    print(f"  zoom csv: {zoom_csv_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
