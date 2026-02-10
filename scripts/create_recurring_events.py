#!/usr/bin/env python3
"""
Create Recurring Events using The Events Calendar Pro API

This script creates recurring events in WordPress using The Events Calendar Pro REST API.
Each event in the series has a unique name and recurs monthly on a specific day pattern
(e.g., first Monday of each month).

Requirements:
- Python 3.6+
- requests library (install with: pip install requests)
- WordPress with The Events Calendar Pro plugin installed
- REST API enabled
- Application password or authentication credentials

Usage:
    python create_recurring_events.py --config config.json
    python create_recurring_events.py --help

@package Collaboration-Area-Event-Series
@version 1.0.0
"""

import argparse
import json
import sys
import time
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description='Create recurring events for The Events Calendar Pro',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_help_epilog()
    )
    parser.add_argument('--config', required=True, help='Path to JSON configuration file')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without actually creating')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    # Create events
    create_recurring_event_series(config, dry_run=args.dry_run, verbose=args.verbose)


def get_help_epilog() -> str:
    """Get help epilog text"""
    return """
Configuration File Format:
{
  "wordpress_url": "https://your-site.com",
  "username": "your-username",
  "app_password": "your-app-password",
  "status": "draft",
  "timezone": "America/New_York",
  "events": [
    {
      "title": "Event Name",
      "description": "Event description",
      "start_date": "2024-01-01",
      "end_date": "2024-12-31",
      "start_time": "14:00:00",
      "end_time": "15:00:00",
      "recurrence_pattern": "MONTHLY",
      "recurrence_day": "first Monday",
      "venue": "Virtual",
      "organizer": "Organization Name",
      "categories": ["Category1", "Category2"],
      "status": "publish",
      "timezone": "America/Los_Angeles"
    }
  ]
}

Recurrence Day Format:
  - "first Monday" - First Monday of each month
  - "second Tuesday" - Second Tuesday of each month
  - "third Wednesday" - Third Wednesday of each month
  - "fourth Thursday" - Fourth Thursday of each month
  - "last Friday" - Last Friday of each month

Optional Global Settings:
  - "status": Event status (default: "draft") - can be "draft" or "publish"
  - "timezone": Event timezone (default: "America/New_York")

Optional Event Settings:
  - Each event can override global "status" and "timezone" settings
  - Example: "status": "publish" in an individual event
"""


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['wordpress_url', 'username', 'app_password', 'events']
    
    for field in required_fields:
        if field not in config:
            print(f"Error: Missing required field '{field}' in config")
            return False
    
    if not isinstance(config['events'], list) or not config['events']:
        print("Error: 'events' must be a non-empty array")
        return False
    
    for index, event in enumerate(config['events']):
        event_required = ['title', 'start_date', 'end_date', 'start_time', 'end_time']
        for field in event_required:
            if field not in event:
                print(f"Error: Event {index} missing required field '{field}'")
                return False
        
        # Validate date format
        try:
            datetime.strptime(event['start_date'], '%Y-%m-%d')
            datetime.strptime(event['end_date'], '%Y-%m-%d')
        except ValueError as e:
            print(f"Error: Invalid date format in event {index}: {e}")
            return False
        
        # Validate time format
        try:
            datetime.strptime(event['start_time'], '%H:%M:%S')
            datetime.strptime(event['end_time'], '%H:%M:%S')
        except ValueError as e:
            print(f"Error: Invalid time format in event {index}: {e}")
            return False
    
    return True


def create_recurring_event_series(config: Dict[str, Any], dry_run: bool = False, verbose: bool = False):
    """
    Create recurring event series
    
    Args:
        config: Configuration dictionary
        dry_run: If True, show what would be created without actually creating
        verbose: Enable verbose output
    """
    wp_url = config['wordpress_url'].rstrip('/')
    api_url = f"{wp_url}/wp-json/tribe/events/v1/events"
    
    auth = (config['username'], config['app_password'])
    
    print("Creating recurring event series...")
    print(f"WordPress URL: {wp_url}")
    print(f"Number of events to create: {len(config['events'])}")
    
    if dry_run:
        print("\n*** DRY RUN MODE - No events will be created ***\n")
    
    print()
    
    success_count = 0
    failure_count = 0
    
    for index, event_data in enumerate(config['events']):
        print(f"Processing event {index + 1}: {event_data['title']}")
        
        try:
            if dry_run:
                print(f"  [DRY RUN] Would create recurring event")
                if verbose:
                    # Build payload to show what would be sent
                    payload = build_event_payload(event_data, config)
                    print(f"  Payload that would be sent:")
                    print(f"  {json.dumps(payload, indent=2)}")
                success_count += 1
            else:
                event_id = create_recurring_event(api_url, auth, event_data, config, verbose)
                if event_id:
                    print(f"  ✓ Successfully created event ID: {event_id}")
                    success_count += 1
                else:
                    print(f"  ✗ Failed to create event")
                    failure_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failure_count += 1
        
        print()
        
        # Small delay to avoid overwhelming the server
        if not dry_run:
            time.sleep(0.5)
    
    print("Summary:")
    print(f"  Successfully created: {success_count}")
    print(f"  Failed: {failure_count}")


def build_event_payload(event_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build the event payload for API submission
    
    Args:
        event_data: Event data dictionary
        config: Global configuration dictionary
    
    Returns:
        Event payload dictionary ready for API submission
    """
    # Prepare recurrence rules
    recurrence_rules = build_recurrence_rules(event_data)
    
    # Get status and timezone with defaults
    # Priority: event-level > global config > defaults
    status = event_data.get('status', config.get('status', 'draft'))
    timezone = event_data.get('timezone', config.get('timezone', 'America/New_York'))
    
    # Prepare event payload
    payload = {
        'title': event_data['title'],
        'description': event_data.get('description', ''),
        'status': status,
        'start_date': f"{event_data['start_date']} {event_data['start_time']}",
        'end_date': f"{event_data['start_date']} {event_data['end_time']}",
        'all_day': False,
        'timezone': timezone,
        'recurrence': recurrence_rules,
    }
    
    # Add optional fields
    if 'venue' in event_data:
        payload['venue'] = {'venue': event_data['venue']}
    
    if 'organizer' in event_data:
        payload['organizer'] = {'organizer': event_data['organizer']}
    
    if 'categories' in event_data:
        payload['categories'] = event_data['categories']
    
    return payload


def create_recurring_event(api_url: str, auth: tuple, event_data: Dict[str, Any], config: Dict[str, Any], verbose: bool = False) -> Optional[int]:
    """
    Create a single recurring event
    
    Args:
        api_url: API endpoint URL
        auth: Tuple of (username, password)
        event_data: Event data dictionary
        config: Global configuration dictionary
        verbose: Enable verbose output
    
    Returns:
        Event ID on success, None on failure
    """
    # Build the payload
    payload = build_event_payload(event_data, config)
    
    if verbose:
        print(f"  Payload: {json.dumps(payload, indent=2)}")
    
    # Make API request
    try:
        response = requests.post(
            api_url,
            json=payload,
            auth=auth,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if verbose:
            print(f"  Response status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            return result.get('id')
        else:
            print(f"  HTTP Error {response.status_code}: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"  Request error: {e}")
        return None


def build_recurrence_rules(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build recurrence rules for the event in The Events Calendar Pro API format
    
    Args:
        event_data: Event data dictionary containing:
            - recurrence_day: Pattern like "first Monday", "second Tuesday" 
                             (optional, defaults to "first Monday")
            - end_date: End date for recurrence in YYYY-MM-DD format (optional)
                       If provided, sets end_type to "On" with the date
                       If omitted, sets end_type to "never"
    
    Returns:
        Recurrence rules dictionary with format:
        {
            'rules': [
                {
                    'type': 'every-month',
                    'on': 'first monday',
                    'end_type': 'never' or 'On',
                    'end': 'YYYY-MM-DD'  # only if end_type is 'On'
                }
            ]
        }
    
    Raises:
        ValueError: If recurrence_day format is invalid
    """
    recurrence_day = event_data.get('recurrence_day', 'first Monday')
    
    # Parse recurrence day (e.g., "first Monday", "second Tuesday")
    match = re.match(
        r'^(first|second|third|fourth|last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$',
        recurrence_day,
        re.IGNORECASE
    )
    
    if not match:
        raise ValueError(f"Invalid recurrence_day format: {recurrence_day}")
    
    position = match.group(1).lower()
    day_of_week = match.group(2).lower()
    
    # Build the "on" field in the format "first monday"
    on_value = f"{position} {day_of_week}"
    
    # Check if there's an end date specified
    end_date = event_data.get('end_date')
    
    # Build the rule object
    rule = {
        'type': 'every-month',
        'on': on_value,
    }
    
    # Add end_type and end date if specified
    if end_date:
        rule['end_type'] = 'On'
        rule['end'] = end_date
    else:
        rule['end_type'] = 'never'
    
    # Build recurrence rule in the format expected by The Events Calendar Pro API
    return {
        'rules': [rule]
    }


if __name__ == '__main__':
    main()
